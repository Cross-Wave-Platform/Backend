from bidict import bidict

SURVEY_TYPE = bidict({'teacher': 1, 'parent': 2, 'relative': 3})
SURVEY_TYPE_CHT = bidict({'教保/教師': 1, '家長': 2, '親友': 3})
AGE_TYPE = bidict({'small': 1, 'big': 2})
AGE_TYPE_CHT = bidict({'小月齡組': 1, '大月齡組': 2})

TRANS_ATTRS={
"file_label":"file_label",
"column_labels":"column_labels",
"variable_value_labels":"variable_value_labels",
"missing_ranges":"missing_ranges",
"variable_display_width":"variable_display_width",
"variable_measure":"variable_measure",
"original_variable_types":"variable_format"}