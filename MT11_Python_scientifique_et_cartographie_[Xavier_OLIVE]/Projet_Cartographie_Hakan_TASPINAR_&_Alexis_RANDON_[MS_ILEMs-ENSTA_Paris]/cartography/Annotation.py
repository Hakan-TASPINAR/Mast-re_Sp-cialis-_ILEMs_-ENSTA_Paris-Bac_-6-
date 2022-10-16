def Annotation(data, row, axis, fontsize):
    axis.annotate(
        data.iloc[row]["TOPONYME"],
        (
            data.iloc[row]["geometry"].coords[0][0],
            data.iloc[row]["geometry"].coords[0][1],
        ),
        fontsize=fontsize,
    )
