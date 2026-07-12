"""Zamiana na wielkie litery

Revision ID: e9e9b4edc2af
Revises: 5574e8cd7a25
Create Date: 2026-07-12 18:59:49.452570

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9e9b4edc2af'
down_revision: Union[str, None] = '5574e8cd7a25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    metadata = sa.MetaData()
    metadata.reflect(bind=bind)

    products = metadata.tables['products']
    brands = metadata.tables['brands']
    models = metadata.tables['models']
    colours = metadata.tables['colours']

    # ==========================================
    # 1. Tabela products (prosta aktualizacja)
    # ==========================================
    all_products = bind.execute(sa.select(
        products.c.id, products.c.brand, products.c.model, products.c.colour
    )).fetchall()
    
    for p_id, p_brand, p_model, p_colour in all_products:
        bind.execute(
            sa.update(products).where(products.c.id == p_id).values(
                brand=p_brand.upper() if p_brand else '',
                model=p_model.upper() if p_model else '',
                colour=p_colour.upper() if p_colour else ''
            )
        )

    # ==========================================
    # 2. Tabela colours (deduplikacja i UPPER)
    # ==========================================
    all_colours = bind.execute(sa.select(colours.c.id, colours.c.name)).fetchall()
    colour_map = {}  # przechowuje mapowanie: ZWIELKOLITEROWANA_NAZWA -> id_do_zachowania
    
    for c_id, c_name in all_colours:
        uname = c_name.upper() if c_name else ''
        if uname not in colour_map:
            # Pierwszy raz widzimy tę nazwę, zapisujemy ją z wielkich liter
            colour_map[uname] = c_id
            bind.execute(sa.update(colours).where(colours.c.id == c_id).values(name=uname))
        else:
            # Nazwa już istnieje (kolizja) - usuwamy duplikat
            bind.execute(sa.delete(colours).where(colours.c.id == c_id))

    # ==========================================
    # 3. Tabela brands (deduplikacja i UPPER)
    # ==========================================
    all_brands = bind.execute(sa.select(brands.c.id, brands.c.name)).fetchall()
    brand_map = {}
    
    for b_id, b_name in all_brands:
        uname = b_name.upper() if b_name else ''
        if uname not in brand_map:
            brand_map[uname] = b_id
            bind.execute(sa.update(brands).where(brands.c.id == b_id).values(name=uname))
        else:
            # Mamy duplikat. Zanim usuniemy markę, musimy upewnić się, 
            # że żaden model nie zostanie "osierocony". Przepinamy klucze obce.
            kept_id = brand_map[uname]
            bind.execute(sa.update(models).where(models.c.brand_id == b_id).values(brand_id=kept_id))
            # Po aktualizacji modeli możemy bezpiecznie usunąć duplikat marki
            bind.execute(sa.delete(brands).where(brands.c.id == b_id))

    # ==========================================
    # 4. Tabela models (deduplikacja, UPPER i NAMEHASH)
    # ==========================================
    all_models = bind.execute(sa.select(models.c.id, models.c.brand_id, models.c.name)).fetchall()
    model_map = {}  # mapowanie: (brand_id, ZWIELKOLITEROWANA_NAZWA) -> id
    
    for m_id, m_brand_id, m_name in all_models:
        uname = m_name.upper() if m_name else ''
        # Klucz unikalny dla modelu zależy od marki i nazwy modelu
        key = (m_brand_id, uname)
        
        if key not in model_map:
            model_map[key] = m_id
            # Generujemy nowy namehash wg wzoru ze zdjęcia: brand_id$^NAME
            new_namehash = f"{m_brand_id}$^{uname}"
            
            bind.execute(
                sa.update(models).where(models.c.id == m_id).values(
                    name=uname,
                    namehash=new_namehash
                )
            )
        else:
            # Duplikat modelu w obrębie tej samej marki - usuwamy
            bind.execute(sa.delete(models).where(models.c.id == m_id))


def downgrade() -> None:
    pass
