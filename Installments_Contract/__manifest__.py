{
    'name': 'Sale installments contract',
    'summary': 'sale with installment contracts',
    'description': """
Sale Installment contract
============================
Auto create or update contract with installment information by adding
a tab on sale order that contains these information.

Usage
--------
1- Check the installment mode option in the SO which will activate the installment contract tab
    - 
2- Enter the installment information as below:
    - advance / down payment amount if any
    - if the down payment a fixed amount check the fixed amount box
    - enter the number of installments ( must be more than 1)
    - enter the repeat every number ( must be more than 0 )
    - select the repeat period ( days , weeks, monthes, years )
    - enter the date of next installment
3- on confirmation of the SO you will get below results:
    - the installment anount will be auto calculated
    - you will get a confirmed invoice of the down payment
    - you will get a contract with recurring invoices representing installments
    - the generated invoices from the contract will be linked to the Sale order
    - the contract start and end dates auto calculated using the date of next installment
    - the contract will be auto closed after reaching end date

Issues/limitations & ToDos:
---------------------------
- limitation: only one SO linked to the contract logically supported, technically many supported but if there's more than one SO linked to the same contract the last SO will get recurring invoices linked to it which will cause accounting issues.
    """,
    'version': '12.0.0.2',
    'category': 'Sales',
    'author': 'Hidext',
     'license': 'AGPL-3',
    "currency": "EUR",
    "price": 12,
    
    'depends': [
        'account_analytic_default',
        'analytic',
        'account',
        'sale',
    ],
    'data': ['static/views.xml'],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
