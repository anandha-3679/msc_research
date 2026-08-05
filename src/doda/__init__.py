"""
doda — Decoupled Operator-Driven Architecture

Shared, importable implementation of the DODA pipeline. Every notebook
(regardless of dataset or author) should import from this package rather
than redefining selectors, the clinical broker, or evaluation logic locally.
This is what keeps results comparable across all four datasets and ensures
a bug fix only needs to happen once.
"""

from .clinical_broker import ClinicalKnowledgeBroker, apply_clinical_weights

__all__ = ["ClinicalKnowledgeBroker", "apply_clinical_weights"]

__version__ = "0.1.0"
