#!/usr/bin/env python3
"""
Script to dump a condensed schema from SQLAlchemy table definitions.
This creates a readable context file showing all tables, columns, types, and foreign keys.

This script automatically discovers all table definition functions in the
cs.infrastructure.sqlalchemy_table_definitions module, so it stays up-to-date
as new tables are added without manual updates.

Usage:
    FOR USE IN case-status-api REPO
    For now run it in that repo & append the output to the AI's context file to update it

    git pull && source environment.env && source dev_environment_variables.sh && alembic upgrade head && python3 dump_schema.py > schema_context.txt

    python dump_schema.py > schema_output.txt
"""

import inspect
from sqlalchemy import MetaData
import cs.infrastructure.sqlalchemy_table_definitions as table_defs


def dump_condensed_schema():
    """
    Generate a condensed schema showing all tables, columns, types, and foreign keys.
    Automatically discovers all table definition functions in the module.
    """
    # Create a metadata object
    metadata = MetaData()
    
    # Automatically discover all table definition functions
    # Look for functions that end with '_table' and are callable
    table_functions = []
    for name, obj in inspect.getmembers(table_defs):
        if (
            inspect.isfunction(obj) 
            and name.endswith('_table') 
            and not name.startswith('_')
        ):
            table_functions.append((name, obj))
    
    # Initialize all tables with the shared metadata
    for table_name, table_func in table_functions:
        try:
            table_func(metadata)
        except Exception as e:
            print(f"Error loading table from {table_name}: {e}")
    
    # Sort tables by name for consistent output
    sorted_tables = sorted(metadata.tables.items())
    
    for table_name, table in sorted_tables:
        print(f"Table: {table_name}")
        
        # Print columns
        for column in table.columns:
            # Get column type
            try:
                column_type = str(column.type)
            except Exception:
                # Fallback for types that can't be compiled (like JSON)
                column_type = column.type.__class__.__name__
            
            # Check for primary key
            pk_marker = " [PK]" if column.primary_key else ""
            
            # Check for foreign keys
            fk_info = ""
            if column.foreign_keys:
                fk_targets = [fk.target_fullname for fk in column.foreign_keys]
                fk_info = f" -> {', '.join(fk_targets)}"
            
            # Check for nullable
            nullable_info = "" if column.nullable else " NOT NULL"
            
            # Print column info
            print(f"  - {column.name}: {column_type}{pk_marker}{nullable_info}{fk_info}")
        
        print()


if __name__ == "__main__":
    dump_condensed_schema()
