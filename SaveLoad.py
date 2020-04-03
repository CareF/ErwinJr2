"""
This file defines functions to save and load JSON files from ErwinJr
"""

from QCLayers import QCLayers
from OptStrata import OptStrata
import json


def qclLoad(fhandle):
    """
    Load QCLayers from a json file

    Parameters
    ----------
    fhandle : file handle
        file handle of a json file to read in

    Returns
    -------
    qclayers : QCLayers.QCLayers
        The QCLayers class described in the json file

    Examples
    --------
    >>> import SaveLoad
    >>> with open("path/to/file.json") as f:
    >>>     qcl = SaveLoad.qclLoad(f)

    """
    ldict = json.load(fhandle)
    return parseQcl(ldict)


def loadBoth(fhandle):
    """
    Load QCLayers and OptStrata from a json file

    Parameters
    ----------
    fhandle : file handle
        file handle of a json file to read in

    Returns
    -------
    qclayers : QCLayers.QCLayers
        The QCLayers class described in the json file
    strata : OptStrata.OptStrata or None
        The Optical Strata class described in the json file. For older version
        this is None

    Examples
    --------
    >>> import SaveLoad
    >>> with open("path/to/file.json") as f:
    >>>     qcl, stratum = SaveLoad.loadBoth(f)

    """
    ldict = json.load(fhandle)
    qcl = parseQcl(ldict)
    try:
        stratum = parseStrata(ldict)
    except NotImplementedError:
        stratum = None
    return qcl, stratum


def parseQcl(ldict):
    if ldict["FileType"] != "ErwinJr2 Data File":
        raise TypeError("Wrong file type")
    if int(ldict["Version"]) >= 181107:
        o = QCLayers(ldict["Substrate"],
                     ldict["Materials"]["Compostion"],
                     ldict["Materials"]["Mole Fraction"],
                     ldict["x resolution"],
                     ldict["E resolution"],
                     ldict["QC Layers"]["Width"],
                     ldict["QC Layers"]["Material"],
                     ldict["QC Layers"]["Doping"],
                     ldict["QC Layers"]["Active Region"],
                     ldict["EField"],
                     ldict["Repeats"],
                     ldict["Temperature"],
                     ldict["Solver"],
                     ldict["Description"])
    else:
        raise NotImplementedError("Version %s not supported" %
                                  ldict["Version"])
    return o


def parseStrata(ldict):
    if ldict["FileType"] != "ErwinJr2 Data File":
        raise TypeError("Wrong file type")
    if int(ldict["Version"]) >= 200403:
        ldict = ldict["Waveguide"]
        cstidx = {}
        for item in ldict["custom"]:
            cstidx[item] = complex(ldict["custom"][item])
        o = OptStrata(ldict["wavelength"],
                      ldict["materials"],
                      ldict["moleFracs"],
                      ldict["dopings"],
                      ldict["width"],
                      ldict["mobilities"],
                      cstidx,
                      ldict["custom Period"])
    else:
        raise NotImplementedError("Version %s not supported" %
                                  ldict["Version"])
    return o


JSONTemplateOld = """{
    "FileType": "ErwinJr2 Data File",
    "Version": "181107",
    "Description": %s,
    "Substrate": %s,
    "EField": %s,
    "x resolution": %s,
    "E resolution": %s,
    "Solver": %s,
    "Temperature": %s,
    "Repeats": %s,
    "Materials": {
        "Compostion": %s,
        "Mole Fraction": %s
    },
    "QC Layers": {
        "Material": %s,
        "Width": %s,
        "Doping": %s,
        "Active Region": %s
    }
}"""


JSONTemplate = """{
    "FileType": "ErwinJr2 Data File",
    "Version": "200403",
    "Description": %s,
    "Substrate": %s,
    "EField": %s,
    "x resolution": %s,
    "E resolution": %s,
    "Solver": %s,
    "Temperature": %s,
    "Repeats": %s,
    "Materials": {
        "Compostion": %s,
        "Mole Fraction": %s
    },
    "QC Layers": {
        "Material": %s,
        "Width": %s,
        "Doping": %s,
        "Active Region": %s
    },
    "Waveguide": {
        "wavelength": %s,
        "materials": %s,
        "moleFracs": %s,
        "dopings": %s,
        "width": %s,
        "mobilities": %s,
        "custom": %s,
        "custom Period": %s
    }
}"""


def qclSaveJSON(fhandle, qclayers):
    """
    Save QCLayers as a json file

    Parameters
    ----------
    fhandle : file handle
        File handle of a json file to save to.
    qclayers : QCLayers.QCLayers
        The QCLayers class to be saved.
    """
    if not isinstance(qclayers, QCLayers):
        raise TypeError("qclSave: Nothing to save.."
                        "QCLayers not valid type")
    o = qclayers
    parameters = [json.dumps(s) for s in (o.description, o.substrate,
                                          o.EField, o.xres, o.Eres, o.Solver,
                                          o.Temperature, o.repeats,
                                          o.materials, o.moleFracs,
                                          o.layerMtrls, o.layerWidths,
                                          o.layerDopings, o.layerARs)]
    fhandle.write(JSONTemplateOld % tuple(parameters))


def EJSaveJSON(fhandle, qclayers, optstratum):
    """Save QCLayers and OptStratum as a json file

    Parameters
    ----------
    fhandle : file handle
        File handle of a json file to save to.
    qclayers : QCLayers.QCLayers
        The QCLayers class to be saved.
    optstratum : OptStrata.OptStratum
        The OptStratum class to be saced
    """
    if not isinstance(qclayers, QCLayers):
        raise TypeError("qclSave: Nothing to save.."
                        "QCLayers not valid type")
    o = qclayers
    s = optstratum
    cstidx = {}
    for item in s.cstmIndx:
        cstidx[item] = str(s.cstmIndx[item])
    parameters = [json.dumps(s) for s in (o.description, o.substrate,
                                          o.EField, o.xres, o.Eres, o.Solver,
                                          o.Temperature, o.repeats,
                                          o.materials, o.moleFracs,
                                          o.layerMtrls, o.layerWidths,
                                          o.layerDopings, o.layerARs,
                                          s.wl, s.materials, s.moleFracs,
                                          s.dopings, list(s.Ls), s.mobilities,
                                          cstidx, s.cstmPrd)]
    fhandle.write(JSONTemplate % tuple(parameters))

# vim: ts=4 sw=4 sts=4 expandtab
