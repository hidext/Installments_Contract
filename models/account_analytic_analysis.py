from dateutil.relativedelta import relativedelta
import datetime
import time

from odoo import models,fields,api
from odoo.tools.translate import _
from logging import getLogger
from odoo.exceptions import ValidationError

_logger = getLogger(__name__)


class account_analytic_default(models.Model):
    _inherit = "account.analytic.account"
    
    installment_mode = fields.Boolean(string = "Installments Mode")
    auto_confirm_invoices = fields.Boolean(string = "Auto Confirm generated Invoices")
    
    
    def _recurring_create_invoice(self,cr,uid,ids,automatic=False, context=None):
        invoice_ids = super(account_analytic_default,self)._recurring_create_invoice(cr, uid, ids, automatic,context=context)
        current_date = time.strftime('%Y-%m-%d')
        
        if not ids:
            ids =  self.search(cr, uid, [
                ('recurring_next_date','<=', current_date),
                ('state', '=','open'),('recurring_invoices','=',True),
                ('type','=','contract')])
        for invoice_obj in self.pool.get('account.invoice').browse(cr, uid, invoice_ids,context=context):
            for account in self.browse(cr, uid, ids, context=context):
                if account.installment_mode:
                    sale_obj =  self.pool.get('sale.order')
                    sale_id = sale_obj.search(cr, uid, [('project_id','=',account.id), ('state','=','manual')], context = context)[0]
                    if sale_id:
                        sale = sale_obj.browse(cr,  uid, sale_id, context=context)
                        
                        if invoice_obj.invoice_line[0] and invoice_obj.invoice_line[0].account_analytic_id == sale.project_id:
                            sale.invoice_ids += invoice_obj
                        if account.recurring_next_date > account.date and account.ca_invoiced == sale.amount_total:
                            account.set_close()
                            sale.signal_workflow('action_invoice_end')
                            sale_obj.write(cr, uid, sale_id,{'state': 'progress'}, context=context)
            if account.auto_confirm_invoices:
                for inv_id in invoice_ids:
                    inv = self.pool['account.invoice'].browse(cr, uid, inv_id, context=context)
                    inv.state == 'draft' and inv.signal_workflow('invoice_open')
        return invoice_ids
                                    
                                    
    
    
    