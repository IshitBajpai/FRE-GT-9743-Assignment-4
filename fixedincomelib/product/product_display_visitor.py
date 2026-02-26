from __future__ import annotations
from atexit import register
from typing import Any, Dict, List, Tuple
import pandas as pd
from functools import singledispatchmethod
from fixedincomelib.product.product_interfaces import Product, ProductVisitor
from fixedincomelib.product.product_portfolio import ProductPortfolio
from fixedincomelib.product.linear_products import (
    ProductBulletCashflow,
    ProductFixedAccrued,
    ProductOvernightIndexCashflow,
    ProductRFRSwap,
)


class ProductDisplayVisitor(ProductVisitor):

    def __init__(self) -> None:
        super().__init__()
        self.nvps_ = []

    @singledispatchmethod
    def visit(self, product: Product):
        raise NotImplementedError(f"No visitor for {type(product)}")

    def display(self) -> pd.DataFrame:
        return pd.DataFrame(self.nvps_, columns=["Name", "Value"])

    # ProductBulletCashflow
    @visit.register
    def _(self, product: ProductBulletCashflow):
        self.nvps_ = []
        self.nvps_.append(("Product Type",     product._product_type))
        self.nvps_.append(("Currency",         product.currency_.value_str))
        self.nvps_.append(("Notional",         product.notional_))
        self.nvps_.append(("Long or Short",    product.long_or_short_.to_string().upper()))
        self.nvps_.append(("Termination Date", product.last_date_.ISO()))
        self.nvps_.append(("Payment Date",     product.paymnet_date_.ISO())) 

    # ProductFixedAccrued
    @visit.register
    def _(self, product: ProductFixedAccrued):
        self.nvps_ = []
        self.nvps_.append(("Product Type",            product._product_type))
        self.nvps_.append(("Currency",                product.currency_.value_str))
        self.nvps_.append(("Notional",                product.notional_))
        self.nvps_.append(("Long or Short",           product.long_or_short_.to_string().upper()))
        self.nvps_.append(("Effective Date",          product.effective_date_.ISO()))
        self.nvps_.append(("Termination Date",        product.termination_date_.ISO()))
        self.nvps_.append(("Accrual Basis",           product.accrual_basis_.value_str))
        self.nvps_.append(("Accrued",                 product.accrued_))
        self.nvps_.append(("Payment Date",            product.paymnet_date_.ISO())) 
        self.nvps_.append(("Business Day Convention", product.business_day_convention_.value_str))
        self.nvps_.append(("Holiday Convention",      product.holiday_convention_.value_str))

    # ProductOvernightIndexCashflow
    @visit.register
    def _(self, product: ProductOvernightIndexCashflow):
        self.nvps_ = []
        self.nvps_.append(("Product Type",       product._product_type))
        self.nvps_.append(("Overnight Index",    product.on_index_str_))
        self.nvps_.append(("Currency",           product.currency_.value_str))
        self.nvps_.append(("Notional",           product.notional_))
        self.nvps_.append(("Long or Short",      product.long_or_short_.to_string().upper()))
        self.nvps_.append(("Effective Date",     product.effective_date_.ISO()))
        self.nvps_.append(("Termination Date",   product.termination_date_.ISO()))
        self.nvps_.append(("Compounding Method", product.compounding_method_.to_string().upper()))
        self.nvps_.append(("Spread",             product.spread_))
        self.nvps_.append(("Payment Date",       product.paymentDate_.ISO())) 

    # ProductRFRSwap
    @visit.register
    def _(self, product: ProductRFRSwap):
        self.nvps_ = []
        self.nvps_.append(("Product Type",                product._product_type))
        self.nvps_.append(("Overnight Index",             product.on_index_str_))
        self.nvps_.append(("Currency",                    product.currency_.value_str))
        self.nvps_.append(("Notional",                    product.notional_))
        self.nvps_.append(("Long or Short",               product.long_or_short_.to_string().upper()))
        self.nvps_.append(("Pay or Receive",              product.pay_or_rec_.to_string().upper()))
        self.nvps_.append(("Effective Date",              product.effective_date_.ISO()))
        self.nvps_.append(("Termination Date",            product.termination_date_.ISO()))
        self.nvps_.append(("Fixed Rate",                  product.fixed_rate_))
        self.nvps_.append(("Fixed Leg Accrual Period",    str(product.accrual_period_)))
        self.nvps_.append(("Fixed Leg Accrual Basis",     product.accrual_basis_.value_str))
        self.nvps_.append(("Floating Leg Accrual Period", str(product.floating_leg_accrual_period_)))
        self.nvps_.append(("Compounding Method",          product.compounding_method_.to_string().upper()))
        self.nvps_.append(("Spread",                      product.spread_))
        self.nvps_.append(("Pay Offset",                  str(product.pay_offset_)))
        self.nvps_.append(("Business Day Convention",     product.pay_business_day_convention_.value_str))
        self.nvps_.append(("Holiday Convention",          product.pay_holiday_convention_.value_str))