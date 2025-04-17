HEADING = """
    .heading_label {
        font-size: 30px;
        margin: 10px 0px;
        line-height: 28px; font-weight: bold;
        color: #0f172a;
    }

    .heading-container {
        border-bottom: 1px solid #e5e7eb;
        padding-bottom: 20px
    }

    .run-button {
        background-color: #1f2937;
        color: white;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 14px;
        font-weight: 600;
        line-height: 20px;
        spacing: 4px;
    }

    .run-button:hover {
        background-color:  #374151;
        border: 1px solid rgba(0, 0, 0, 0.1);
    }

    .run-button:pressed {
        background-color: #111827;
    }

    .run-dialog {
        border: 2px solid #3498db;
        border-radius: 8px;
        background-color: white;
        border-radius: 6px;
        padding: 20px 16px;
        color: #111827;
        font-size: 14px;
        line-height: 20px;
        font-weight: 600;
    }

    .run-combo {
        background-color: white;
        color: #111827;
        font-size: 14px;
        border: 1px solid #d1d5db;
        border-radius: 6px;
        padding: 6px 12px;
        min-width: 120px;
        text-align: left;
    }

    .run-combo::dropdown {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left: 1px solid #d1d5db;
        border-top-right-radius: 6px;
        border-bottom-right-radius: 6px;
    }

    .run-combo:hover {
        border-color: #9ca3af;
    }

    .run-combo:focus {
        border-color: #4f46e5;
        border-width: 2px;
    }

    QComboBox QAbstractItemView {
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        background-color: white;
        padding: 4px 0;
        margin-top: 4px;
        selection-background-color: #4f46e5;
        selection-color: white;
        outline: none;
    }

    QComboBox QAbstractItemView::item {
        padding: 8px 12px;
        color: #111827;
    }

    /* Selected item highlight */
    QComboBox QAbstractItemView::item:selected {
        background-color: #4f46e5
        color: white;
    }

    /* Checkmark for selected item */
    QComboBox QAbstractItemView::indicator {
        width: 16px;
        height: 16px;
    }
"""


FORM_LABEL = """
    QLabel {
        font-size: 14px;
        font-weight: 500;
        color: #111827;
        margin-bottom: 4px;
    }
"""
