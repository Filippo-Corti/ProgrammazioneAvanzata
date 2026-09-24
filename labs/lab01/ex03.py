CELSIUS = "Celsius"
FAHRENEIT = "Fahreneit"
KELVIN = "Kelvin"
RANKINE = "Rankine"
DELISLE = "Delisle"
NEWTON = "Newton"
REAUMUR = "Reaumur"
ROMER = "Romer"


scales = [CELSIUS, FAHRENEIT, KELVIN, RANKINE, DELISLE, NEWTON, REAUMUR, ROMER]
uom = {
    CELSIUS: "°C",
    FAHRENEIT: "°F",
    KELVIN: "K",
    RANKINE: "°R",
    DELISLE: "°De",
    NEWTON: "°N",
    REAUMUR: "°Re",
    ROMER: "°Ro",
}


kelvin_to_any = {
    CELSIUS: lambda x: (x - 273.15),
    FAHRENEIT: lambda x: (x * 9 / 5 - 459.67),
    KELVIN: lambda x: x,
    RANKINE: lambda x: (x * 9 / 5),
    DELISLE: lambda x: (373.15 - x) * 3 / 2,
    NEWTON: lambda x: (x - 273.15) * 33 / 100,
    REAUMUR: lambda x: (x - 273.15) * 4 / 5,
    ROMER: lambda x: ((x - 273.15) * 21 / 40 + 7.5),
}

any_to_kelvin = {
    CELSIUS: lambda x: (x + 273.15),
    FAHRENEIT: lambda x: (x + 459.67) * 5 / 9,
    KELVIN: lambda x: x,
    RANKINE: lambda x: (x * 5 / 9),
    DELISLE: lambda x: (373.15 - x * 2 / 3),
    NEWTON: lambda x: (x * 100 / 33 + 273.15),
    REAUMUR: lambda x: (x * 5 / 4 + 273.15),
    ROMER: lambda x: ((x - 7.5) * 40 / 21 + 273.15),
}

convert = lambda n, fr, to: kelvin_to_any[to](any_to_kelvin[fr](n))

# 1)


def table(n, colsize=12):
    tablerow = lambda l: "|" + "|".join(l) + "|\n"

    header = tablerow(f"{s:^{colsize}}" for s in scales)
    hline = tablerow(["-" * colsize] * len(scales))

    return (
        hline
        + header
        + hline
        + "".join(
            tablerow(
                f"{convert(n, fromscale, toscale):+{colsize}.3f}" for toscale in scales
            )
            for fromscale in scales
        )
        + hline
    )


# 2)


def toAll(n, scale):
    if scale not in scales:
        raise Exception("Unknown scale")

    conversions = sorted(
        (
            (convert(n, scale, toscale), toscale)
            for toscale in scales
            if toscale != scale
        ),
        key=lambda x: x[0],
    )

    return f"{n} {uom[scale]} = " + "; ".join(
        f"{val:+.3f} {uom[s]}" for val, s in conversions
    )


NUMBER = 56
print(table(NUMBER, colsize=12))
print(toAll(NUMBER, CELSIUS))
