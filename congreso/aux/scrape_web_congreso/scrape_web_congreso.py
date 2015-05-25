# Scrape seats positions of Congreso from 
#   http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/Hemiciclo
#
#   Image:
#       http://www.congreso.es/wc/htdocs/web/img/hemiciclo/hemiciclo.gif

from lxml import html
import re
import json
import os.path as path
import codecs

SOURCE_FILE = path.join("sources", "hemiciclo.html")
URL = "http://www.congreso.es"
OUTPUT_DIR = "json"
FILE_OUT_by_seat_code = path.join(OUTPUT_DIR, "chamber_by_seat.json")
FILE_OUT_by_politician_name = path.join(OUTPUT_DIR, "chamber_by_politician.json")

print "Generating files: ", FILE_OUT_by_seat_code, FILE_OUT_by_politician_name

###############################################
# LOAD & PARSE html file
###############################################
tree = None;
with open(SOURCE_FILE) as f:
    tree = html.fromstring(
        f.read()
        )


###############################################
# PROCESS <div id=""> nodes
#   Generates a map: seat_coords_by_politician
###############################################
areas = tree.xpath("//div[@id='capaHemiciclo']/map/area")

def for_each_area(accumulator, item):
    # Politician name
    _politician_name = item.xpath("@alt")[0]
    politician_name = _politician_name.split("(")[0].strip()

    # Seat coordinates
    _seat_coords = item.xpath("@coords")
    seat_coords = _seat_coords[0].split(",")[:2]


    # Build 
    accumulator[politician_name] = {
        "coords" : seat_coords,
        "name" : politician_name
        }
    return accumulator
seat_coords_by_politician = reduce(for_each_area, areas, {})
    

###############################################
# PROCESS <div id="datosHemiciclo"> nodes
###############################################
"""
<noscript>

    <div>

        
                
                
                    <div id="datosHemiciclo">
                        <div class="fotoDiputado">
                            <img src="/wc/htdocs/web/img/diputados/peq/118_10.jpg" onError="" alt="Mato Adrover, Ana (Ministra de Sanidad, Servicios Sociales e Igualdad)"/>
                        </div>
                        <div class="datosDiputado">
                            <div class="nombreDiputado">
                                
                                        <a href="/portal/page/portal/Congreso/Congreso/Diputados/BusqForm?_piref73_1333155_73_1333154_1333154.next_page=/wc/fichaDiputado&idDiputado=118&idLegislatura=10">Mato Adrover, Ana (Ministra de Sanidad, Servicios Sociales e Igualdad)</a>.
                                
                            </div>
                            
                                <div class="otrosDiputado">
                                    Diputada por Madrid eoooooooo.
                                </div>
                            
                            
                                <div class="otrosDiputado">
                                    G.P. Popular.
                                </div>
                            
                            
                                
                                        <div class="otrosDiputado">
                                            Zona:1
                                        </div>
                                        <div class="otrosDiputado">
                                            Fila:1
                                        </div>
                                        <div class="otrosDiputado">
                                            Asiento:06
                                        </div>
                                
                                 #
                        </div>
                    </div>
                                
"""

diputados = tree.xpath("//div[@id='datosHemiciclo']")

def for_each_diputado(acc, item):

    # MP's picture
    _foto_src = item.xpath("div[@class='fotoDiputado']/img/@src")
    if isinstance(_foto_src, list) and len(_foto_src) > 0:
        foto_src = "%s%s" % (URL, _foto_src[0])
    else:
        foto_src = URL

    # Page
    _page = item.xpath("div[@class='datosDiputado']/div[@class='nombreDiputado']/a/@href")
    if isinstance(_page, list) and len(_page) > 0:
        page = "%s%s" % (URL, _page[0])
    else:
        page = URL

    # Name and role/group
    _name_and_role_or_group = item.xpath("div[@class='datosDiputado']/div[@class='nombreDiputado']/a/text()")
    if isinstance(_name_and_role_or_group, list) and len(_name_and_role_or_group) > 0:
        name_and_role_or_group = _name_and_role_or_group[0]
    else:
        # Retry: maybe the name is not wrapped by an <a> element
        _name_and_role_or_group = item.xpath("div[@class='datosDiputado']/div[@class='nombreDiputado']/text()")
        if isinstance(_name_and_role_or_group, list) and len(_name_and_role_or_group) > 0:
            name_and_role_or_group = _name_and_role_or_group[0]
        else:
            name_and_role_or_group = ""
            
    regex = re.compile("([^(]*)[(](.*)[)]")
    m = regex.search(name_and_role_or_group)
    name = m.groups()[0].strip()
    role_or_group = m.groups()[1]

    #
    # Rest of field are <div class="otrosDiputado">
    #
    _otros = item.xpath("div[@class='datosDiputado']/div[@class='otrosDiputado']/text()")
    otros = "".join(_otros)
    

    # Provincia
    regex_otros_provincia = re.compile(r"""
        .*Diputad[ao][ ]por[ ]*(.*)[ ]*eo.*  # Provincia
        """,re.VERBOSE)
    m = regex_otros_provincia.search(otros)
    if m:
        provincia = m.groups("")[0]
    else:
        provincia = ""

    # Grupo parlamentario
    regex_otros_grupo_parlamentario = re.compile(r"""
        .*G.P.[ ]*(.*)[. ]
        """,re.VERBOSE)
    m = regex_otros_grupo_parlamentario.search(otros)
    if m:
        grupo_parlamentario = m.groups("")[0]
    else:
        grupo_parlamentario = ""

    # Zona
    regex_otros_zona = re.compile(r"""
        [Zz]ona:(\d+)  
        """,re.VERBOSE)
    m = regex_otros_zona.search(otros)
    if m:
        zona = m.groups("0")[0]
    else:
        zona = "0"

    # Fila
    regex_otros_fila = re.compile(r"""
        [Ff]ila:(\d+)  
        """,re.VERBOSE)
    m = regex_otros_fila.search(otros)
    if m:
        fila = m.groups("0")[0]
    else:
        fila = "0"
    
    # Asiento
    regex_otros_asiento = re.compile(r"""
        [Aa]siento:(\d+)  
        """,re.VERBOSE)
    m = regex_otros_asiento.search(otros)
    if m:
        asiento = m.groups("00")[0]
    else:
        asiento = "00"

    # Asiento codificado
    asiento_cod = "%01d%01d%02d" % (int(zona),int(fila),int(asiento))
    assert isinstance(asiento_cod, str) 
    assert len(asiento_cod) == 4 
    assert int(asiento_cod) < 5999

    # Seat coords from map: seat_coords_by_politician
    coords = seat_coords_by_politician[name]["coords"]

    acc[name] = {
        "name"  : name,
        "foto_src"  : foto_src,
        "page"      : page,
        "role_or_group" : role_or_group,
        "province"  :   provincia,
        "group" : grupo_parlamentario,
        "seat_code"  : asiento_cod,
        "seat_coords"   : coords
        }
    return acc

def build_index_by_seat_code(acc, item):
    key, value = item
    acc[value["seat_code"]] = value
    return acc

###############################################
# build & write maps to file in JSON format
###############################################
map_by_politician = reduce(for_each_diputado, diputados,{})
map_by_seat_code = reduce(build_index_by_seat_code, map_by_politician.items(), {})


map_by_politician_json =  json.dumps(map_by_politician, ensure_ascii=False, encoding="utf-8",
    sort_keys=True, indent=4, separators=(',', ': '))
with codecs.open(FILE_OUT_by_politician_name, "w", encoding="utf-8")as f:
    f.write(map_by_politician_json)

map_by_seat_code_json =  json.dumps(map_by_seat_code, ensure_ascii=False, encoding="utf-8",
    sort_keys=True, indent=4, separators=(',', ': '))
with codecs.open(FILE_OUT_by_seat_code, "w", encoding="utf-8")as f:
    f.write(map_by_seat_code_json)


