from decimal import Decimal
from .Constants_aCommon import Calendar, Precision, PrecisionAtts
from .Moment_aUniversal import UnivMoment

import bisect

GEOLOGICAL_TIME_STRUCTURE = {
    "Source": "https://rock.geosociety.org/net/documents/gsa/timescale/timescl.pdf",
    "Title": "Geological Time Scale",
    "version": "6.0",
    "download-date": "2024-06-10",
    "units": "millions of years ago (Ma)",
    "note": "The time scale is divided into hierarchical units: eons, eras, periods, epochs and ages. The Phanerozoic Eon is subdivided into three eras: Paleozoic, Mesozoic, and Cenozoic. The Precambrian is a term that encompasses the Hadean, Archean, and Proterozoic eons.",
    "pre-phanerozoic": [
        {
            "name": "Precambrian",
            "start": 4550,
            "end": 541,
            "eons": [
                {"name": "Hadean", "start": 4550, "end": 4000},
                {
                    "name": "Archean",
                    "start": 4000,
                    "end": 2500,
                    "eras": [
                        {"name": "Eoarchean", "start": 4000, "end": 3600},
                        {"name": "Paleoarchean", "start": 3600, "end": 3200},
                        {"name": "Mesoarchean", "start": 3200, "end": 2800},
                        {"name": "Neoarchean", "start": 2800, "end": 2500},
                    ],
                },
                {
                    "name": "Proterozic",
                    "start": 2500,
                    "end": 541,
                    "eras": [
                        {
                            "name": "Paleoproterozoic",
                            "start": 2500,
                            "end": 1600,
                            "periods": [
                                {"name": "Siderian", "start": 2500, "end": 2300},
                                {"name": "Rhyacian", "start": 2300, "end": 2050},
                                {"name": "Orosirian", "start": 2050, "end": 1800},
                                {"name": "Statherian", "start": 1800, "end": 1600},
                            ],
                        },
                        {
                            "name": "Mesoproterozoic",
                            "start": 1600,
                            "end": 1000,
                            "periods": [
                                {"name": "Calymmian", "start": 1600, "end": 1400},
                                {"name": "Ectasian", "start": 1400, "end": 1200},
                                {"name": "Stenian", "start": 1200, "end": 1000},
                            ],
                        },
                        {
                            "name": "Neoproterozoic",
                            "start": 1000,
                            "end": 541,
                            "periods": [
                                {"name": "Tonian", "start": 1000, "end": 720},
                                {"name": "Cryogenian", "start": 720, "end": 635},
                                {"name": "Ediacaran", "start": 635, "end": 541},
                            ],
                        },
                    ],
                },
            ],
        }
    ],
    "eons": [
        {
            "name": "Phanerozoic",
            "start": 541.0,
            "end": None,
            "eras": [
                {
                    "name": "Paleozoic",
                    "start": 541.0,
                    "end": 251.90,
                    "periods": [
                        {
                            "name": "Cambrian",
                            "start": 541.0,
                            "end": 485.4,
                            "epochs": [
                                {
                                    "name": "Terreneuvian",
                                    "start": 541.0,
                                    "end": 521,
                                    "ages": [
                                        {
                                            "name": "Fortunuan",
                                            "start": 541.0,
                                            "end": 529,
                                        },
                                        {"name": "Age 2", "start": 529, "end": 521},
                                    ],
                                },
                                {
                                    "name": "Epoch 2",
                                    "start": 521,
                                    "end": 509,
                                    "ages": [
                                        {"name": "Age 3", "start": 521, "end": 514},
                                        {"name": "Age 4", "start": 514, "end": 509},
                                    ],
                                },
                                {
                                    "name": "Mialolingian",
                                    "start": 509,
                                    "end": 497,
                                    "ages": [
                                        {"name": "Wuliuan", "start": 509, "end": 504.5},
                                        {
                                            "name": "Drumian",
                                            "start": 504.5,
                                            "end": 500.5,
                                        },
                                        {
                                            "name": "Guzhangian",
                                            "start": 500.5,
                                            "end": 497,
                                        },
                                    ],
                                },
                                {
                                    "name": "Furongian",
                                    "start": 497,
                                    "end": 485.4,
                                    "ages": [
                                        {"name": "Paibian", "start": 497, "end": 494},
                                        {
                                            "name": "Jiangshanianan",
                                            "start": 494,
                                            "end": 489.5,
                                        },
                                        {
                                            "name": "Age 10",
                                            "start": 489.5,
                                            "end": 485.4,
                                        },
                                    ],
                                },
                            ],
                        },
                        {
                            "name": "Ordovician",
                            "start": 485.4,
                            "end": 443.8,
                            "epochs": [
                                {
                                    "name": "Early",
                                    "start": 485.4,
                                    "end": 470,
                                    "ages": [
                                        {
                                            "name": "Tremadocian",
                                            "start": 485.4,
                                            "end": 477.7,
                                        },
                                        {"name": "Floian", "start": 477.7, "end": 470},
                                    ],
                                },
                                {
                                    "name": "Middle",
                                    "start": 470,
                                    "end": 458.4,
                                    "ages": [
                                        {
                                            "name": "Dapingian",
                                            "start": 470,
                                            "end": 467.3,
                                        },
                                        {
                                            "name": "Darriwilian",
                                            "start": 467.3,
                                            "end": 458.4,
                                        },
                                    ],
                                },
                                {
                                    "name": "Late",
                                    "start": 458.4,
                                    "end": 443.8,
                                    "ages": [
                                        {
                                            "name": "Sandbian",
                                            "start": 458.4,
                                            "end": 453.0,
                                        },
                                        {
                                            "name": "Katian",
                                            "start": 453.0,
                                            "end": 445.2,
                                        },
                                        {
                                            "name": "Hirnantian",
                                            "start": 445.2,
                                            "end": 443.8,
                                        },
                                    ],
                                },
                            ],
                        },
                        {
                            "name": "Silurian",
                            "start": 443.8,
                            "end": 419.2,
                            "epochs": [
                                {
                                    "name": "Llandovery",
                                    "start": 443.8,
                                    "end": 433.4,
                                    "ages": [
                                        {
                                            "name": "Rhuddanian",
                                            "start": 443.8,
                                            "end": 440.8,
                                        },
                                        {
                                            "name": "Aeronian",
                                            "start": 440.8,
                                            "end": 438.5,
                                        },
                                        {
                                            "name": "Telychian",
                                            "start": 438.5,
                                            "end": 433.4,
                                        },
                                    ],
                                },
                                {
                                    "name": "Wenlock",
                                    "start": 433.4,
                                    "end": 427.4,
                                    "ages": [
                                        {
                                            "name": "Sheinwoodian",
                                            "start": 433.4,
                                            "end": 430.5,
                                        },
                                        {
                                            "name": "Homerian",
                                            "start": 430.5,
                                            "end": 427.4,
                                        },
                                    ],
                                },
                                {
                                    "name": "Ludlow",
                                    "start": 427.4,
                                    "end": 423.0,
                                    "ages": [
                                        {
                                            "name": "Gorstian",
                                            "start": 427.4,
                                            "end": 425.6,
                                        },
                                        {
                                            "name": "Ludfordian",
                                            "start": 425.6,
                                            "end": 423.0,
                                        },
                                    ],
                                },
                                {"name": "Pridoli", "start": 423.0, "end": 419.2},
                            ],
                        },
                        {
                            "name": "Devonian",
                            "start": 419.2,
                            "end": 358.9,
                            "epochs": [
                                {
                                    "name": "Early",
                                    "start": 419.2,
                                    "end": 393.3,
                                    "ages": [
                                        {
                                            "name": "Lochkovian",
                                            "start": 419.2,
                                            "end": 410.8,
                                        },
                                        {
                                            "name": "Pragian",
                                            "start": 410.8,
                                            "end": 407.6,
                                        },
                                        {
                                            "name": "Emsian",
                                            "start": 407.6,
                                            "end": 393.3,
                                        },
                                    ],
                                },
                                {
                                    "name": "Middle",
                                    "start": 393.3,
                                    "end": 382.7,
                                    "ages": [
                                        {
                                            "name": "Eifelian",
                                            "start": 393.3,
                                            "end": 387.7,
                                        },
                                        {
                                            "name": "Givetian",
                                            "start": 387.7,
                                            "end": 382.7,
                                        },
                                    ],
                                },
                                {
                                    "name": "Late",
                                    "start": 382.7,
                                    "end": 358.9,
                                    "ages": [
                                        {
                                            "name": "Frasnian",
                                            "start": 382.7,
                                            "end": 372.2,
                                        },
                                        {
                                            "name": "Famennian",
                                            "start": 372.2,
                                            "end": 358.9,
                                        },
                                    ],
                                },
                            ],
                        },
                        {
                            "name": "Carboniferous",
                            "start": 358.9,
                            "end": 289.9,
                            "epochs": [
                                {
                                    "name": "Mississippian",
                                    "start": 358.9,
                                    "end": 323.2,
                                    "ages": [
                                        {
                                            "name": "Tournaisain",
                                            "start": 358.9,
                                            "end": 346.7,
                                        },
                                        {
                                            "name": "Visean",
                                            "start": 346.7,
                                            "end": 330.9,
                                        },
                                        {
                                            "name": "Serpukhovian",
                                            "start": 330.9,
                                            "end": 323.2,
                                        },
                                    ],
                                },
                                {
                                    "name": "Pennsylvanian",
                                    "start": 323.2,
                                    "end": 298.9,
                                    "ages": [
                                        {
                                            "name": "Bashkirian",
                                            "start": 323.2,
                                            "end": 315.2,
                                        },
                                        {
                                            "name": "Moscovian",
                                            "start": 315.2,
                                            "end": 307.0,
                                        },
                                        {
                                            "name": "Kasimovian",
                                            "start": 307.0,
                                            "end": 303.7,
                                        },
                                        {
                                            "name": "Gzhelian",
                                            "start": 303.7,
                                            "end": 298.9,
                                        },
                                    ],
                                },
                            ],
                        },
                        {
                            "name": "Permian",
                            "start": 298.9,
                            "end": 251.90,
                            "epochs": [
                                {
                                    "name": "Cisuralian",
                                    "start": 298.9,
                                    "end": 273.01,
                                    "ages": [
                                        {
                                            "name": "Asselian",
                                            "start": 298.9,
                                            "end": 293.52,
                                        },
                                        {
                                            "name": "Sakamarian",
                                            "start": 293.52,
                                            "end": 290.1,
                                        },
                                        {
                                            "name": "Artinskian",
                                            "start": 290.1,
                                            "end": 283.5,
                                        },
                                        {
                                            "name": "Kungurian",
                                            "start": 283.5,
                                            "end": 273.01,
                                        },
                                    ],
                                },
                                {
                                    "name": "Guadalupian",
                                    "start": 273.01,
                                    "end": 259.51,
                                    "ages": [
                                        {
                                            "name": "Roadian",
                                            "start": 273.01,
                                            "end": 266.9,
                                        },
                                        {
                                            "name": "Wordian",
                                            "start": 266.9,
                                            "end": 264.28,
                                        },
                                        {
                                            "name": "Capitanian",
                                            "start": 264.28,
                                            "end": 259.51,
                                        },
                                    ],
                                },
                                {
                                    "name": "Lopingian",
                                    "start": 259.51,
                                    "end": 251.90,
                                    "ages": [
                                        {
                                            "name": "Wuchiapingian",
                                            "start": 259.51,
                                            "end": 254.14,
                                        },
                                        {
                                            "name": "Changhsingian",
                                            "start": 254.14,
                                            "end": 251.90,
                                        },
                                    ],
                                },
                            ],
                        },
                    ],
                },
                {
                    "name": "Mesozoic",
                    "start": 251.90,
                    "end": 66.0,
                    "periods": [
                        {
                            "name": "Triassic",
                            "start": 251.90,
                            "end": 201.3,
                            "epochs": [
                                {
                                    "name": "Early",
                                    "start": 251.90,
                                    "end": 247.2,
                                    "ages": [
                                        {
                                            "name": "Induan",
                                            "start": 251.90,
                                            "end": 251.2,
                                        },
                                        {
                                            "name": "Olenekian",
                                            "start": 251.2,
                                            "end": 247.2,
                                        },
                                    ],
                                },
                                {
                                    "name": "Middle",
                                    "start": 247.2,
                                    "end": 237,
                                    "ages": [
                                        {"name": "Anisian", "start": 247.2, "end": 242},
                                        {"name": "Ladinian", "start": 242, "end": 237},
                                    ],
                                },
                                {
                                    "name": "Late",
                                    "start": 237,
                                    "end": 201.3,
                                    "ages": [
                                        {"name": "Carnian", "start": 237, "end": 227},
                                        {"name": "Norian", "start": 227, "end": 208.5},
                                        {
                                            "name": "Rhaetian",
                                            "start": 208.5,
                                            "end": 201.3,
                                        },
                                    ],
                                },
                            ],
                        },
                        {
                            "name": "Jurassic",
                            "start": 201.3,
                            "end": 145,
                            "epochs": [
                                {
                                    "name": "Early",
                                    "start": 201.3,
                                    "end": 174.1,
                                    "ages": [
                                        {
                                            "name": "Hettangian",
                                            "start": 201.4,
                                            "end": 199.3,
                                        },
                                        {
                                            "name": "Sinermurian",
                                            "start": 199.3,
                                            "end": 190.8,
                                        },
                                        {
                                            "name": "Pliensbachian",
                                            "start": 190.8,
                                            "end": 182.7,
                                        },
                                        {
                                            "name": "Toarcian",
                                            "start": 182.7,
                                            "end": 174.1,
                                        },
                                    ],
                                },
                                {
                                    "name": "Middle",
                                    "start": 174.1,
                                    "end": 163.5,
                                    "ages": [
                                        {
                                            "name": "Aalenian",
                                            "start": 174.1,
                                            "end": 170.3,
                                        },
                                        {
                                            "name": "Bajocian",
                                            "start": 170.3,
                                            "end": 168.3,
                                        },
                                        {
                                            "name": "Bathonian",
                                            "start": 168.3,
                                            "end": 166.1,
                                        },
                                        {
                                            "name": "Callovian",
                                            "start": 166.1,
                                            "end": 163.5,
                                        },
                                    ],
                                },
                                {
                                    "name": "Late",
                                    "start": 163.5,
                                    "end": 145.0,
                                    "ages": [
                                        {
                                            "name": "Oxfordian",
                                            "start": 163.5,
                                            "end": 157.3,
                                        },
                                        {
                                            "name": "Kimmeridgian",
                                            "start": 157.3,
                                            "end": 152.1,
                                        },
                                        {
                                            "name": "Tithonian",
                                            "start": 152.1,
                                            "end": 145.0,
                                        },
                                    ],
                                },
                            ],
                        },
                        {
                            "name": "Cretaceous",
                            "start": 145.0,
                            "end": 66.0,
                            "epochs": [
                                {
                                    "name": "Early",
                                    "start": 145.0,
                                    "end": 100.5,
                                    "ages": [
                                        {
                                            "name": "Berriasian",
                                            "start": 145.0,
                                            "end": 139.8,
                                        },
                                        {
                                            "name": "Valanginian",
                                            "start": 139.8,
                                            "end": 132.6,
                                        },
                                        {
                                            "name": "Hauterivian",
                                            "start": 132.6,
                                            "end": 129.4,
                                        },
                                        {
                                            "name": "Barremian",
                                            "start": 129.4,
                                            "end": 125,
                                        },
                                        {"name": "Aptian", "start": 125, "end": 113},
                                        {
                                            "name": "Aalenian",
                                            "start": 113,
                                            "end": 100.5,
                                        },
                                    ],
                                },
                                {
                                    "name": "Late",
                                    "start": 100.5,
                                    "end": 66.0,
                                    "ages": [
                                        {
                                            "name": "Cenomanian",
                                            "start": 100.5,
                                            "end": 93.9,
                                        },
                                        {
                                            "name": "Turonian",
                                            "start": 93.9,
                                            "end": 89.8,
                                        },
                                        {
                                            "name": "Conician",
                                            "start": 89.8,
                                            "end": 86.3,
                                        },
                                        {
                                            "name": "Santonian",
                                            "start": 86.3,
                                            "end": 83.6,
                                        },
                                        {
                                            "name": "Campanian",
                                            "start": 83.6,
                                            "end": 72.1,
                                        },
                                        {
                                            "name": "Maastrichtian",
                                            "start": 72.1,
                                            "end": 66.0,
                                        },
                                    ],
                                },
                            ],
                        },
                    ],
                },
                {
                    "name": "Cenozoic",
                    "start": 66.0,
                    "end": None,
                    "periods": [
                        {
                            "name": "(tertiary)Paleogene",
                            "start": 66.0,
                            "end": 23.03,
                            "epochs": [
                                {
                                    "name": "Paleocene",
                                    "start": 65.0,
                                    "end": 56.0,
                                    "ages": [
                                        {"name": "Danian", "start": 65.0, "end": 61.6},
                                        {
                                            "name": "Selandian",
                                            "start": 61.6,
                                            "end": 59.2,
                                        },
                                        {
                                            "name": "Thanetian",
                                            "start": 59.2,
                                            "end": 56.0,
                                        },
                                    ],
                                },
                                {
                                    "name": "Eocene",
                                    "start": 56.0,
                                    "end": 33.9,
                                    "ages": [
                                        {
                                            "name": "Ypresian",
                                            "start": 56.0,
                                            "end": 47.8,
                                        },
                                        {
                                            "name": "Lutetian",
                                            "start": 47.8,
                                            "end": 41.2,
                                        },
                                        {
                                            "name": "Bartonian",
                                            "start": 41.2,
                                            "end": 37.71,
                                        },
                                        {
                                            "name": "Priabonian",
                                            "start": 37.71,
                                            "end": 33.9,
                                        },
                                    ],
                                },
                                {
                                    "name": "Oligocene",
                                    "start": 33.9,
                                    "end": 23.03,
                                    "ages": [
                                        {
                                            "name": "Rupelian",
                                            "start": 33.9,
                                            "end": 27.82,
                                        },
                                        {
                                            "name": "Chattian",
                                            "start": 27.82,
                                            "end": 23.03,
                                        },
                                    ],
                                },
                            ],
                        },
                        {
                            "name": "(tertiary)Neogene",
                            "start": 23.03,
                            "end": 2.58,
                            "epochs": [
                                {
                                    "name": "Miocene",
                                    "start": 23.03,
                                    "end": 5.333,
                                    "ages": [
                                        {
                                            "name": "Aquitanian",
                                            "start": 23.02,
                                            "end": 20.44,
                                        },
                                        {
                                            "name": "Burdigalian",
                                            "start": 20.44,
                                            "end": 15.97,
                                        },
                                        {
                                            "name": "Langhian",
                                            "start": 15.97,
                                            "end": 13.82,
                                        },
                                        {
                                            "name": "Serravallian",
                                            "start": 13.82,
                                            "end": 11.63,
                                        },
                                        {
                                            "name": "Tortonian",
                                            "start": 11.63,
                                            "end": 7.246,
                                        },
                                        {
                                            "name": "Messinian",
                                            "start": 7.246,
                                            "end": 5.333,
                                        },
                                    ],
                                },
                                {
                                    "name": "Pliocene",
                                    "start": 5.333,
                                    "end": 2.58,
                                    "ages": [
                                        {
                                            "name": "Zanclean",
                                            "start": 5.333,
                                            "end": 3.600,
                                        },
                                        {
                                            "name": "Piacenzian",
                                            "start": 3.600,
                                            "end": 2.58,
                                        },
                                    ],
                                },
                            ],
                        },
                        {
                            "name": "Quarternary",
                            "start": 2.58,
                            "end": None,
                            "epochs": [
                                {
                                    "name": "Pleistocene",
                                    "start": 2.58,
                                    "end": 0.0117,
                                    "ages": [
                                        {"name": "Gelasian", "start": 2.58, "end": 1.8},
                                        {
                                            "name": "Calabrian",
                                            "start": 1.8,
                                            "end": 0.774,
                                        },
                                        {
                                            "name": "Chibanian",
                                            "start": 0.774,
                                            "end": 0.129,
                                        },
                                        {
                                            "name": "Age 4",
                                            "start": 0.129,
                                            "end": 0.0117,
                                        },
                                    ],
                                },
                                {
                                    "name": "Holocene",
                                    "start": 0.0117,
                                    "end": None,
                                    "ages": [
                                        {
                                            "name": "Greenlandian",
                                            "start": 0.0117,
                                            "end": 0.0082,
                                        },
                                        {
                                            "name": "Northgrippian",
                                            "start": 0.0082,
                                            "end": 0.0042,
                                        },
                                        {
                                            "name": "Meghalayan",
                                            "start": 0.0042,
                                            "end": None,
                                        },
                                    ],
                                },
                            ],
                        },
                    ],
                },
            ],
        }
    ],
}


GEOLOGICAL_EONS = []
GEOLOGICAL_ERAS = []
GEOLOGICAL_PERIODS = []
GEOLOGICAL_EPOCHSandAGES = []


class Present_Geological(UnivMoment.Presentation):
    """
    Geological calendar representation of a UnivMoment.
    """
    # CONSTRUCTOR ############################################################################
    def __init__(self, moment: UnivMoment):
        if (PrecisionAtts[moment.precision]["level"] > PrecisionAtts[Precision.YEAR]["level"]):
            raise ValueError("Geological moments must have precision of at least year or coarser.")
        if moment == UnivMoment.beginning_of_time():
            year = Decimal('-inf')
        else:
            year = (moment.rd_day / Decimal('365.25')).to_integral_value(rounding='ROUND_FLOOR')
        super().__init__(Calendar.GEOLOGICAL, moment, year)
        return

    # PRESENTATION LAYER METHODS ############################################################
    """
    def strftime(self, format: str, language: str = "en") -> str:

    Format the Moment using a custom format string.
    This is a simplified version and does not support all Python strftime features.

    Geological
    Directive	Meaning	                            Example
                YEAR
    %Y	        Julian style                   	    66.45 M-yr BCE
    %y	        Gregorian style                     -66.45 M-yr

                EON
    %O	        full name                    	    Cenozoic, Archean
    
                ERA
    %R	        full name                    	
    
                PERIODS
    %P	        full name

                small AGES or EPOCHS
    %a	        full name

    %K          calender system name	            Geological
    %k          calender                	        GE
    Modifiers
    
    """
    def _format_segment(self, segment : dict, language : str) -> str:
        seg_type = segment['type']
        #eliminate_leading_zero = segment.get('eliminate_leading_zero', False)
        # 
        if seg_type in 'Yy':
            """
            Format the year component based on the segment type and language.
            """
            if self.precision == Precision.BILLION_YEARS:
                year = f"{self.year / 1_000_000_000:.2f}"
            elif self.precision == Precision.MILLION_YEARS:
                year = f"{self.year / 1_000_000:.2f}"
            elif self.precision == Precision.THOUSAND_YEARS:
                year = f"{self.year / 1_000:.2f}"
            elif self.precision == Precision.YEAR:
                year = f"{self.year}"
            else:
                raise ValueError("Year is not defined for the current precision level.")
            # Handle negative vales
            fmt = year
            if seg_type == "Y":
                if (PrecisionAtts[self.precision]["level"] < PrecisionAtts[Precision.YEAR]["level"]):
                    fmt += f" {PrecisionAtts[self.precision]['abbrv']}"
            elif seg_type == "y":
                if (PrecisionAtts[self.precision]["level"] < PrecisionAtts[Precision.YEAR]["level"]):
                    fmt += f" {PrecisionAtts[self.precision]['abbrv']}"
            return fmt
        elif seg_type in 'O':
            """
            Format the EONs Component 
            """
            global GEOLOGICAL_EONS

            def key_func(x):
                return x["start"]["year"]

            ins_pnt = (
                bisect.bisect_left(
                    [key_func(item) for item in GEOLOGICAL_EONS], self.year
                )
                - 1
            )
            if ins_pnt < 0:
                return "EON before the big-bang"
            period = GEOLOGICAL_EONS[ins_pnt]
            return period["name"] if period else "Unknown eon"
        elif seg_type in 'R':
            """
            Format the ERAs Component 
            """
            global GEOLOGICAL_ERAS

            def key_func(x):
                return x["start"]["year"]

            ins_pnt = (
                bisect.bisect_left(
                    [key_func(item) for item in GEOLOGICAL_ERAS], self.year
                )
                - 1
            )
            if ins_pnt < 0:
                return "pre-eras"
            period = GEOLOGICAL_ERAS[ins_pnt]
            return period["name"] if period else "Unknown era"
        elif seg_type == "P":
            """
            Format the PERIODSs Component 
            """
            global GEOLOGICAL_PERIODS

            def key_func(x):
                return x["start"]["year"]

            ins_pnt = (
                bisect.bisect_left(
                    [key_func(item) for item in GEOLOGICAL_PERIODS], self.year
                )
                - 1
            )
            if ins_pnt < 0:
                return "pre-periods"
            period = GEOLOGICAL_PERIODS[ins_pnt]
            return period["name"] if period else "Unknown period"
        elif seg_type == "a":
            """
            Format the small epochs and ages Component 
            """
            global GEOLOGICAL_EPOCHSandAGES

            def key_func(x):
                return x["start"]["year"]

            ins_pnt = (
                bisect.bisect_left(
                    [key_func(item) for item in GEOLOGICAL_EPOCHSandAGES], self.year
                )
                - 1
            )
            if ins_pnt < 0:
                return "pre-epochs"
            period = GEOLOGICAL_EPOCHSandAGES[ins_pnt]
            return period["name"] if period else "Unknown epoch"
        else:
            return f'%{seg_type}'  # Unknown segment, return as is
        

def main():
    global \
        GEOLOGICAL_EONS, \
        GEOLOGICAL_ERAS, \
        GEOLOGICAL_PERIODS, \
        GEOLOGICAL_EPOCHSandAGES

    def convert_time(
        year: Decimal | int | float, precision: Precision, description: str = ""
    ) -> dict:
        if isinstance(year, (int, float)):
            year = Decimal(str(year))
        else:
            pass
        if year <0:
            raise ValueError("Geological time scale entries must be non-negative")
        if precision != Precision.MILLION_YEARS:
            raise ValueError(
                "Geological time scale entries must have million year precision"
            )
        year = -year * Decimal('1_000_000')
        return {"year": year, "description": description}

    # Created a start, end time sorted list of geological periods
    def create_eons(
        eons: list,
        eras: list,
        periods: list,
        epochs: list,
        start_date: Decimal,
        eon_list: list,
    ) -> Decimal:
        eon_end = float("-inf")
        for eon in eon_list:
            eon_name = eon.get("name", None)
            if eon_name is None:
                raise ValueError(
                    "Invalid file 'geological-time-scale.json' - missing eon name"
                )
            eon_start = eon["start"]
            if eon_start is None:
                raise ValueError(f"Eon {eon_name} has no start date")
            eon_start = convert_time(
                eon_start, precision=Precision.MILLION_YEARS, description=eon_name
            )
            eon_end = eon.get("end", float("+inf"))
            if eon_end:
                eon_end = convert_time(
                    eon_end, precision=Precision.MILLION_YEARS, description=eon_name
                )
            eons.append(
                {
                    "type": "eon",
                    "name": eon_name,
                    "start": eon_start,
                    "end": eon_end,
                }
            )
            if "eras" in eon:
                create_eras(
                    eon_name, eras, periods, epochs, eon_start, eon.get("eras", [])
                )
        return eon_end

    def create_eras(
        eon_name: str,
        eras: list,
        periods: list,
        epochs: list,
        start_date: Decimal,
        era_list: list,
    ) -> Decimal:
        era_end = float("-inf")
        for era in era_list:
            era_name = era.get("name", None)
            if era_name is None:
                raise ValueError(
                    f"Invalid file 'geological-time-scale.json' - missing era name in {eon_name}"
                )
            era_start = era["start"]
            if era_start is None:
                raise ValueError(f"Era {era_name} has no start date")
            era_start = convert_time(
                era_start, precision=Precision.MILLION_YEARS, description=era_name
            )
            era_end = era.get("end", float("+inf"))
            if era_end:
                era_end = convert_time(
                    era_end, precision=Precision.MILLION_YEARS, description=era_name
                )
            eras.append(
                {
                    "type": "era",
                    "name": era_name,
                    "eon": eon_name,
                    "start": era_start,
                    "end": era_end,
                }
            )
            if "periods" in era:
                create_periods(
                    era, era_name, periods, epochs, era_start, era.get("periods", [])
                )
        return era_end

    def create_periods(
        eon_name: str,
        era_name,
        periods: list,
        epochs: list,
        start_date: Decimal,
        period_list: list,
    ) -> Decimal:
        period_end = float("-inf")
        for period in period_list:
            period_name = period.get("name", None)
            if period_name is None:
                raise ValueError(
                    f"Invalid file 'geological-time-scale.json' - missing period name in {era_name}"
                )
            period_start = period["start"]
            if period_start is None:
                raise ValueError(f"Period {period_name} has no start date")
            period_start = convert_time(
                period_start, precision=Precision.MILLION_YEARS, description=period_name
            )
            period_end = period.get("end", float("+inf"))
            if period_end:
                period_end = convert_time(
                    period_end,
                    precision=Precision.MILLION_YEARS,
                    description=period_name,
                )
            periods.append(
                {
                    "type": "period",
                    "name": period_name,
                    "eon": eon_name,
                    "era": era_name,
                    "start": period_start,
                    "end": period_end,
                }
            )
            if "epochs" in period:
                create_epochs(
                    eon_name,
                    era_name,
                    period_name,
                    epochs,
                    period_start,
                    period.get("epochs", []),
                )
        return period_end

    def create_epochs(
        eon_name: str,
        era_name,
        period_name: str,
        epochs: list,
        start_date: Decimal,
        epoch_list: list,
    ) -> Decimal:
        epoch_end = float("-inf")
        for epoch in epoch_list:
            epoch_name = epoch.get("name", None)
            if epoch_name is None:
                raise ValueError(
                    f"Invalid file 'geological-time-scale.json' - missing period name in {era_name}"
                )
            epoch_start = epoch["start"]
            if epoch_start is None:
                raise ValueError(f"Period {epoch_name} has no start date")
            epoch_start = convert_time(
                epoch_start, precision=Precision.MILLION_YEARS, description=epoch_name
            )
            epoch_end = epoch.get("end", float("+inf"))
            if epoch_end:
                epoch_end = convert_time(
                    epoch_end, precision=Precision.MILLION_YEARS, description=epoch_name
                )

            if "ages" in epoch:
                create_ages(
                    eon_name,
                    era_name,
                    period_name,
                    epoch_name,
                    epochs,
                    epoch_start,
                    epoch.get("ages", []),
                )
            else:
                epochs.append(
                    {
                        "type": "period",
                        "name": epoch_name,
                        "eon": eon_name,
                        "era": era_name,
                        "period": period_name,
                        "start": epoch_start,
                        "end": epoch_end,
                    }
                )
        return epoch_end

    def create_ages(
        eon_name: str,
        era_name: str,
        period_name: str,
        epoch_name: str,
        epochs: list,
        start_date: Decimal,
        ages_list: list,
    ) -> Decimal:
        age_end = float("-inf")
        for age in ages_list:
            age_name = age.get("name", None)
            if age_name is None:
                raise ValueError(
                    f"Invalid file 'geological-time-scale.json' - missing age name in {epoch_name}"
                )
            age_start = age["start"]
            if age_start is None:
                raise ValueError(f"Period {age_name} has no start date")
            age_start = convert_time(
                age_start, precision=Precision.MILLION_YEARS, description=age_name
            )
            age_end = age.get("end", float("+inf"))
            if age_end:
                age_end = convert_time(
                    age_end, precision=Precision.MILLION_YEARS, description=age_name
                )

            epochs.append(
                {
                    "type": "epoch-age",
                    "name": epoch_name.lower() + " " + age_name,
                    "eon": eon_name,
                    "era": era_name,
                    "period": period_name,
                    "epoch": epoch_name,
                    "start": age_start,
                    "end": age_end,
                }
            )
        return age_end

    GEOLOGICAL_EONS = []
    GEOLOGICAL_ERAS = []
    GEOLOGICAL_PERIODS = []
    GEOLOGICAL_EPOCHSandAGES = []

    begin_earth = convert_time(4550, Precision.MILLION_YEARS, "Earth formation era")
    pre_cam = GEOLOGICAL_TIME_STRUCTURE.get("pre-phanerozoic", [None])[0]
    last_date = create_eons(
        GEOLOGICAL_EONS,
        GEOLOGICAL_ERAS,
        GEOLOGICAL_PERIODS,
        GEOLOGICAL_EPOCHSandAGES,
        begin_earth,
        pre_cam.get("eons", []),
    )
    last_date = create_eons(
        GEOLOGICAL_EONS,
        GEOLOGICAL_ERAS,
        GEOLOGICAL_PERIODS,
        GEOLOGICAL_EPOCHSandAGES,
        last_date,
        GEOLOGICAL_TIME_STRUCTURE.get("eons", []),
    )

    # Sort end date, then start date
    GEOLOGICAL_EONS.sort(
        key=lambda period: period["end"]["year"] if period["end"] else float("-inf")
    )
    GEOLOGICAL_EONS.sort(
        key=lambda period: period["start"]["year"] if period["start"] else float("-inf")
    )
    return


try:
    main()
except Exception as e:
    print(f"Error creating geological periods: {e}")
