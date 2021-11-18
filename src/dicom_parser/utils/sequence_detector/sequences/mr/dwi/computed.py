DWI_COMPUTED_RULES = [
    {
        "key": "ImageType",
        "value": ["DERIVED", "PRIMARY", "DIFFUSION", "ND", "NORM"],
        "lookup": "in",
        "operator": "all",
    },
    {
        "key": "ImageType",
        "value": ["FA", "ADC", "TRACEW"],
        "lookup": "in",
        "operator": "any",
    },
]
