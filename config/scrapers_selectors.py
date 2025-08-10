# -*- coding: utf-8 -*-
"""
CSS selectors for scrapers
- don't forget to escape slash bar into css selector
- insert None for a css selector when you are using hook to scrape this particular data for a scraper
"""
from typing import Optional, Dict, TypedDict


class SelectorFields(TypedDict, total=False):
    reference:Optional[str]
    asset_type:Optional[str]
    contract:Optional[str]
    disponibility:Optional[str]
    area:Optional[str]
    division:Optional[str]
    adress:Optional[str]
    building_name:Optional[str]
    title:Optional[str]
    contact:Optional[str]
    resume:Optional[str]
    amenities:Optional[str]
    prestations:Optional[str]
    url_image:Optional[str]
    latitude:Optional[str]
    longitude:Optional[str]
    global_price:Optional[str]
    global_rent:Optional[str]


SELECTORS: Dict[str, SelectorFields] = {
    "BNP": {
        "reference": "#presentation > div > div.col.s12.offer-hero--left > div.offer-hero--left--middle > div.line.space-between.share-businessid-line.hidden-mobile.hidden-tablet > div.line.mobile-column > div.business-id > p",
        "asset_type": None,
        "contract": None,
        "disponibility": "#columns-container > div:nth-child(1) > ul > li > p > span",
        "area": "#presentation > div > div.col.s12.offer-hero--left > div.offer-hero--left--middle > div.surface-block.line.no-padding.flex-column > div.surface > p > span:nth-child(1)",
        "division": "#presentation > div > div.col.s12.offer-hero--left > div.offer-hero--left--middle > div.surface-block.line.no-padding.flex-column > div.surface > p > span.divisible",
        "adress": "#presentation > div > div.col.s12.offer-hero--left > div.offer-hero--left--middle > div.commercial-title > h1 > p",
        "building_name": "#presentation > div > div.col.s12.offer-hero--left > div.offer-hero--left--middle > div.commercial-title > h1 > span:nth-child(2)",
        "contact": "#block-bnpre-content > article > div.node__content.clearfix > div.offer-content > div > div.col.s12.l5.xl4.offer-content--right > div > div.card.card-contact > div > div:nth-child(2) > p.h3",
        "resume": "#description > div > p:nth-child(3)",
        "amenities": "#columns-container",
        "url_image": None,
        "latitude": None,
        "longitude": None,
        "global_price": "#presentation > div > div.col.s12.offer-hero--left > div.offer-hero--left--bottom.hidden-mobile > div > div.block-budget.line.align-center.vente.active > div > p",
        "global_rent": "#presentation > div > div.col.s12.offer-hero--left > div.offer-hero--left--bottom.hidden-mobile > div > div.block-budget.line.align-center.location.active > div > p",
    },
    "JLL": {
        "reference": "#propertySummary > div > div.col-span-12.lg\\:col-span-10 > div > div.flex.items-center.justify-between.gap-4.max-\\[575px\\]\\:flex-col-reverse > div.flex.items-center.justify-center.gap-4.max-\\[575px\\]\\:flex-col-reverse > span",
        "asset_type": None,
        "contract": None,
        "disponibility": "#propertySummary > div > div.col-span-12.lg\\:col-span-10 > div > div.mt-4.flex.items-start.sm\\:mt-9 > div.flex-1.\\[\\&\\:not\\(\\:last-child\\)\\]\\:mr-11 > ul > li:nth-child(2) > span.text-lg.text-neutral-700",
        "area": "#propertySummary > div > div.col-span-12.lg\\:col-span-10 > div > div.mt-4.flex.items-start.sm\\:mt-9 > div.flex-1.\\[\\&\\:not\\(\\:last-child\\)\\]\\:mr-11 > ul > li:nth-child(1) > span.text-lg.text-neutral-700 > span > span:nth-child(1)",
        "division": "#propertySummary > div > div.col-span-12.lg\\:col-span-10 > div > div.mt-4.flex.items-start.sm\\:mt-9 > div.flex-1.\\[\\&\\:not\\(\\:last-child\\)\\]\\:mr-11 > ul > li:nth-child(1) > span.text-lg.text-neutral-700 > span > span:nth-child(1) > span",
        "adress": "head > title",
        "contact": "#propertySummary > div > div.col-span-12.lg\\:col-span-10 > div > div.mt-4.flex.items-start.sm\\:mt-9 > div.inline-flex.items-center.justify-center.whitespace-nowrap.rounded.text-sm.font-semibold.ring-offset-white.transition-colors.focus-visible\\:outline-none.focus-visible\\:ring-2.focus-visible\\:ring-neutral-950.focus-visible\\:ring-offset-2.disabled\\:pointer-events-none.disabled\\:opacity-50.text-neutral-900.underline-offset-4.hover\\:underline.h-9.px-4.py-1.\\!justify-start.\\!no-underline.mb-1.h-full.w-full.\\!rounded-md.border.bg-white.px-4.py-3.hover\\:bg-white.hover\\:shadow-md.hidden.max-w-44.cursor-pointer.lg\\:block > div.overflow-hidden.text-left > p.overflow-hidden.text-ellipsis.text-base.font-bold",
        "resume": "#description > div > div > p",
        "amenities": "#amenities > div > ul",
        "global_price": "#propertySummary > div > div.col-span-12.lg\\:col-span-10 > div > div.mt-4.flex.items-start.sm\\:mt-9 > div.flex-1.\\[\\&\\:not\\(\\:last-child\\)\\]\\:mr-11 > div.mb-6.flex.flex-col.flex-wrap.items-center.justify-between.text-center.sm\\:flex-row.sm\\:text-left > div.flex.items-center.justify-end.text-bronze.\\[\\&_p\\]\\:text-2xl.\\[\\&_p\\]\\:font-semibold > p",
    },
    "CBRE": {
        "reference": None,
        "asset_type": None,
        "contract": None,
        "disponibility": "#contentHolder_availability",
        "area": "#contentHolder_surface",
        "division": "#contentHolder_surfaceDiv",
        "adress": "#contentHolder_address1",
        "contact": "#contentHolder_contactZone.row.contact-person > div.col-9.info > p:nth-child(2)",
        "resume": "#section-description > p:nth-child(3)",
        "amenities": "#section-feature > div > div:nth-child(1) > p",
        "prestations": "#contentHolder_featureZone > ul",
        "url_image": None,
        "latitude": None,
        "longitude": None,
        "global_price": "#contentHolder_price",
    },
    "ALEXBOLTON": {
        "reference": "body > section.listing-header.py-md-4 > div > div > div.col-lg-5.position-relative > div > div.bolton-header-5.bolton-grey.mb-2",
        "asset_type": None,
        "contract": "body > section.listing-header.py-md-4 > div > div > div.col-lg-5.position-relative > div > div.d-flex.gap-4.mb-4 > div:nth-child(1) > p:nth-child(1)",
        "disponibility": "body > section.listing-header.py-md-4 > div > div > div.col-lg-5.position-relative > div > div.d-flex.gap-4.mb-4 > div:nth-child(2) > p:nth-child(2)",
        "area": "body > section.listing-header.py-md-4 > div > div > div.col-lg-5.position-relative > div > div.d-flex.gap-4.mb-4 > div:nth-child(1) > p:nth-child(4)",
        "division": None,
        "adress": "body > section.listing-header.py-md-4 > div > div > div.col-lg-5.position-relative > div > div.bolton-header-4.mb-4",
        "building_name": "body > section.listing-header.py-md-4 > div > div > div.col-lg-5.position-relative > div > h1",
        "resume": None,
        "contact": "body > section.listing-details.bolton-bg-grey.u-py-80.u-py-mobile-24 > div > div > div.col-lg-4.position-relative > div > h3",
        "amenities": "body > section.listing-details.bolton-bg-grey.u-py-80.u-py-mobile-24 > div > div > div.col-lg-8 > div.d-flex > div > div.listing-details-description.mb-3",
        "url_image": None,
        "latitude": None,
        "longitude": None,
        "global_price": "body > section.listing-header.py-md-4 > div > div > div.col-lg-5.position-relative > div > div.d-flex.gap-4.mb-4 > div:nth-child(1) > p:nth-child(2)",
    },
    "CUSHMANWAKEFIELD": {
        "reference": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(1) > div > header > p.u-t.u-t--sm.u-t-additional",
        "asset_type": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(1) > div > header > p.c-property__category",
        "contract": None,
        "contract": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(1) > div > header > p.c-property__category",
        "disponibility": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(3) > p:nth-child(3) > span.u-t--tertiary",
        "area": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(3) > p:nth-child(1) > span.u-t--tertiary",
        "division": "None",
        "adress": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(1) > div > header > h1",
        # On peut utiliser le span pour séparer nom et prénom
        "contact": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(4) > div > div > div.c-contact__main > h5",
        "resume": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(2) > div > section:nth-child(5) > p",
        "amenities": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(2) > div > section:nth-child(7) > ul",
        "url_image": None,
        "latitude": None,
        "longitude": None,
        "global_price": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(3) > div > div > p > span.u-t--tertiary",
    },
    "KNIGHTFRANK": {
        "reference": "body > main > section > div.container.p-lg-0.contOMob > div > div.col-xl-7.p-xl-0.p-0 > div:nth-child(1) > div > ol > li:nth-child(5) > a > span",
        "asset_type": None,
        "contract": None,
        "disponibility": "body > main > section > div.container.p-lg-0.contOMob > div > div.col-xl-7.p-xl-0.p-0 > div.row.pb-4.align-items-center.p24 > div.col-xl-4.col-md-4.col-12.cDisp > div > p",
        "area": "body > main > section > div.container.p-lg-0.contOMob > div > div.col-xl-7.p-xl-0.p-0 > div.row.pb-4.align-items-center.p24 > div.col-xl-4.col-md-4.col-auto.pe-0 > div > p.valeur-offre",
        "division": "body > main > section > div.container.p-lg-0.contOMob > div > div.col-xl-7.p-xl-0.p-0 > div.row.pb-4.align-items-center.p24 > div.col-xl-4.col-md-4.col-auto.pe-0 > div > p.post-text-offre > span",
        "adress": None,
        "contact": "body > main > section > div.container.p-lg-0.contOMob > div > div.d-none.col-xl-3.offset-xl-1.p-xl-0.pt-xl-4.pt-4.d-xl-flex.relative.p24 > div > div.blocAgent > div > div.offset-1.col-7.p-0.d-flex.flex-column.justify-content-center.ml-3 > p",
        "resume": "body > main > section > div.container.p-lg-0.contOMob > div > div.col-xl-7.p-xl-0.p-0 > div:nth-child(4) > div > p.offreDesc",
        "amenities": "body > main > section > div.container.p-lg-0.contOMob > div > div.col-xl-7.p-xl-0.p-0 > div:nth-child(8) > div > div > ul",
        "url_image": None,
        "latitude": None,
        "longitude": None,
        "global_price": "body > main > section > div.container.p-lg-0.contOMob > div > div.col-xl-7.p-xl-0.p-0 > div.row.pb-4.align-items-center.p24 > div.col-xl-4.col-md-4.col-auto.ps-0 > div > p.valeur-offre",
    },
    "ARTHURLOYD": {
        "reference": "#advisor-brick-wrapper > div > div:nth-child(1) > div.offer-informations.d-flex.align-items-center.justify-content-between > div.reference > b",
        "asset_type": None,
        "contract": None,
        "disponibility": None,
        "area": "#details-desktop > div > div.col-xl-2.d-none.d-xl-block.text-end > div > div > a > div.max-surface > span",
        "division": "#details-desktop > div > div.col-xl-2.d-none.d-xl-block.text-end > div > div > a > div.d-flex.justify-content-end.min-surface > div:nth-child(1) > span.surface",
        "adress": "#localisation > div",
        "title": "#advisor-brick-wrapper > div > div:nth-child(1) > div.offer-title",
        "contact": "#advisor-brick-wrapper > div > div.advisor-card > div > div > div.advisor-informations > div > div:nth-child(1) > div:nth-child(1) > span",
        "resume": "#description > div > div > div > div > div:nth-child(2) > p",
        "amenities": "#amenities > section > div > div > div:nth-child(1) > div > ul",
        "url_image": None,
        "latitude": None,
        "longitude": None,
        "global_price": "#advisor-brick-wrapper > div > div:nth-child(1) > div:nth-child(3) > div > ul > li:nth-child(3) > span.price",
    },
}

""" Add a css selectors dict for a new scraper
"SCRAPER" : {
    "reference": None,
    "asset_type": None,
    "contract": None,
    "disponibility": None,
    "area": None,
    "division": None,
    "adress": None,
    "contact": None,
    "accroche": None,
    "amenagements": None,
    "global_price": None
}
"""
