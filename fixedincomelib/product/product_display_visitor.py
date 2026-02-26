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
        self.nvps_ = [
            ("Product Type",     product._product_type),
            ("Currency",         product.currency_.value_str),
            ("Notional",         product.notional_),
            ("Long or Short",    product.long_or_short_.to_string().upper()),
            ("Termination Date", product.last_date_.ISO()),
            ("Payment Date",     product.paymnet_date_.ISO()),  # note: typo in source
        ]

    # ProductFixedAccrued
    @visit.register
    def _(self, product: ProductFixedAccrued):
        self.nvps_ = [
            ("Product Type",            product._product_type),
            ("Currency",                product.currency_.value_str),
            ("Notional",                product.notional_),
            ("Long or Short",           product.long_or_short_.to_string().upper()),
            ("Effective Date",          product.effective_date_.ISO()),
            ("Termination Date",        product.termination_date_.ISO()),
            ("Accrual Basis",           product.accrual_basis_.value_str),
            ("Accrued",                 product.accrued_),
            ("Payment Date",            product.paymnet_date_.ISO()),  # note: typo in source
            ("Business Day Convention", product.business_day_convention_.value_str),
            ("Holiday Convention",      product.holiday_convention_.value_str),
        ]

    # ProductOvernightIndexCashflow
    @visit.register
    def _(self, product: ProductOvernightIndexCashflow):
        self.nvps_ = [
            ("Product Type",       product._product_type),
            ("Overnight Index",    product.on_index_str_),
            ("Currency",           product.currency_.value_str),
            ("Notional",           product.notional_),
            ("Long or Short",      product.long_or_short_.to_string().upper()),
            ("Effective Date",     product.effective_date_.ISO()),
            ("Termination Date",   product.termination_date_.ISO()),
            ("Compounding Method", product.compounding_method_.to_string().upper()),
            ("Spread",             product.spread_),
            ("Payment Date",       product.paymentDate_.ISO()),  # note: camelCase in source
        ]

    # ProductRFRSwap
    @visit.register
    def _(self, product: ProductRFRSwap):
        self.nvps_ = [
            ("Product Type",                product._product_type),
            ("Overnight Index",             product.on_index_str_),
            ("Currency",                    product.currency_.value_str),
            ("Notional",                    product.notional_),
            ("Long or Short",               product.long_or_short_.to_string().upper()),
            ("Pay or Receive",              product.pay_or_rec_.to_string().upper()),
            ("Effective Date",              product.effective_date_.ISO()),
            ("Termination Date",            product.termination_date_.ISO()),
            ("Fixed Rate",                  product.fixed_rate_),
            ("Fixed Leg Accrual Period",    str(product.accrual_period_)),
            ("Fixed Leg Accrual Basis",     product.accrual_basis_.value_str),
            ("Floating Leg Accrual Period", str(product.floating_leg_accrual_period_)),
            ("Compounding Method",          product.compounding_method_.to_string().upper()),
            ("Spread",                      product.spread_),
            ("Pay Offset",                  str(product.pay_offset_)),
            ("Business Day Convention",     product.pay_business_day_convention_.value_str),
            ("Holiday Convention",          product.pay_holiday_convention_.value_str),
        ]