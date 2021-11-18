DWI_COMPUTED_RULES = [
    {
        "key": "ImageType",
        "value": ["DERIVED", "PRIMARY", "DIFFUSION", "ND"],
        "lookup": "in",
        "operator": "all",
    },
    {
        "key": "ImageType",
        "value": ["FA", "ADC", "TRACEW", "TENSOR"],
        "lookup": "in",
        "operator": "any",
    },
]
