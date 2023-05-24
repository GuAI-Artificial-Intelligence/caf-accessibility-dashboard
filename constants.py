from dash import html


BOGOTA_STR = 'Bogotá'
CUENCA_STR = 'Cuenca'

CENTER_CITY_COORDINATES = {
    BOGOTA_STR: {
        'center_lat': 4.7110,
        'center_lon': -74.0721
    },
    CUENCA_STR: {
        'center_lat': -2.891889142459372,
        'center_lon': -78.9889487554136
    }
}
ACCESIBILITY_MEANS = {
    "A pie": "accessibility_foot",
    "Bicicleta": "accessibility_bicycle",
    "Carro": "accessibility_car",
}

# Components IDs
BELOW_GRAPH_ID = "below-graph"
MAP_ID = 'my-map'
CITY_SELECTOR = 'my-city-selector'
ACCESIBILITY_SELECTOR = 'my-accesibility-selector'
CATEGORY_SELECTOR = 'my-category-selector'
VARIABLE_SELECTOR = 'my-variable-selector'
TRANSPORT_MODE_SELECTOR = 'my-transport-mode-selector'
INFRA_CHECKLIST_ID = 'infra-checklist'
BELOW_TABS = 'below-tabs'

CATEGORICAL_VARIABLES = ['IndiAcce_1', 'NSE_5']
NON_CATEGORICAL_VARIABLES = ['Poblacion']
GEO_VARIABLES = ['geometry']

TRANSPORT_MODES = ['Todos', 'A pie', 'Bicicleta', 'Carro']

# POPULATION_TYPES = {
#     'TOT_POB': 'Toda la poblacion',
#     'ANALF': 'Personas analfabetas',
#     'DISCAP': 'Personas discapacitadas',
#     'MUJER_JEF_HOG': 'Mujeres jefas de hogar',
#     'INDIGENAS': 'Indígenas',
#     'AFRO': 'Afrodescendientes',
# }

POPULATION_TYPES = {
    'TOT_POB': 'Toda la poblacion',
    'PEATON': 'Peatones',
    'BICIUSUARIO': 'Biciusuarios',
    'MUJERES': 'Mujeres',
    'MOVILIDAD_CUIDADO': 'Dificultad para moverse',
    # 'DIFIC_BICI': 'Dificultad para usar bicicleta',
    # 'DIFIC_AUTO': 'Dificultad para usar automóvil',
    # 'DIFIC_BUS': 'Dificultad para usar bus/microbús',
    # 'DIFIC_TRANSMILENIO': 'Dificultad para usar TransMilenio',

}

MAP_BELOW_TAB_ACCESSIBILITY = {
    'TOT_POB': 'Poblacion',
    'PEATON': 'peaton',
    'BICIUSUARIO': 'bicicleta',
    'MUJERES': 'mujer',
    'MOVILIDAD_CUIDADO': 'movilidad_cuidado',
    # 'DIFIC_BICI': 'p9_id_dificultad_medios_transporte_11',
    # 'DIFIC_AUTO': 'p9_id_dificultad_medios_transporte_2',
    # 'DIFIC_BUS': 'p9_id_dificultad_medios_transporte_4',
    # 'DIFIC_TRANSMILENIO': 'p9_id_dificultad_medios_transporte_5',

}

# MAP_BELOW_TAB_ACCESSIBILITY = {
#     'TOT_POB': 'Poblacion',
#     'ANALF': 'Cant_PersAnalf',
#     'DISCAP': 'Cant_PersDiscap',
#     'MUJER_JEF_HOG': 'Mujeres_Jefas_Hogar',
#     'INDIGENAS': 'Indigenas',
#     'AFRO': 'Afrodescendientes',
# }

NSE_3_DICTMAP = {
    '1 - Alto': 3,
    '2 - Medio': 2,
    '3 - Bajo': 1
}

NSE_5_DICTMAP = {
    '1 - Alto': 5,
    '2 - Medio-Alto': 4,
    '3 - Medio': 3,
    '4 - Medio-Bajo': 2,
    '5 - Bajo': 1
}

INDIACCE_DICTMAP = {
    '1. Alta': 4,
    '2. Media Alta': 3,
    '3. Media Baja': 2,
    '4. Baja': 1
}

# NS3_COLORSCALE = ['#311a3c', '#b63c3f', '#daa98a']
NS3_TICKVALS = [1, 2, 3]
NS3_TICKTEXT = ['Bajo',  'Medio', 'Alto']

# NS5_COLORSCALE = ['#b23d37','#c37a3b','#95b14f','#5ebc4b',]
NS5_TICKVALS = [1, 2, 3, 4, 5]
NS5_TICKTEXT = ['Bajo', 'Medio-Bajo', 'Medio', 'Medio-Alto', 'Alto']

INDIACCE_TICKVALS = [1, 2, 3, 4]
INDIACCE_TICKTEXT = ['Baja', 'Media Baja', 'Media Alta', 'Alta']
# INDIACCE_COLORSCALE = ['#b23d37', '#c37a3b', '#95b14f', '#5ebc4b',]
INDIACCE_COLORSCALE = ['#b23d37', '#c37a3b', '#95b14f', '#3a8447',]


CATEGORICAL_COLORBAR = dict(
    orientation='v',
    thickness=10,
    y=0.2,
    x=0.86,
    len=0.3,
    tickfont=dict(color="#323232"),
)

HIDDEN_COLORBAR = dict(
    orientation='h',
    thickness=1,
    y=0.0,
    x=0.0,
    len=0.05,
    tickfont=dict(color="rgba(0,0,0,0)",
                  size=10)
)

HIDDEN_COLORSCALE = ['#1b4332', '#1b4332', '#1b4332', '#1b4332']

ACERCA_DE_BODY_CONTENT = html.Div(
    children=[
        html.H5(
            "Antecedentes¹",
            className="card-title",
            style={'margin-bottom': '16px',
                   'font-size': '24px'}
        ),
        html.P(
            "La accesibilidad urbana se refiere a la facilidad con la que los habitantes de una ciudad pueden acceder a bienes, servicios, actividades y destinos. Esta accesibilidad está condicionada por factores como la desigualdad territorial y el sistema de movilidad en la ciudad. Por lo tanto, características como la disponibilidad de transporte público, la distancia a los centros importantes y la propiedad de un vehículo particular, pueden afectar la accesibilidad de los ciudadanos y favorecer a ciertos grupos socioeconómicos sobre otros.",
            style={'line-height': '1.2',
                   'font-size': '15px', 'margin-bottom': '16px'}
        ),
        html.P(
            "El análisis de accesibilidad es clave para entender cómo las personas acceden a oportunidades urbanas desde diferentes partes de la ciudad. La accesibilidad es un tema transversal en los Objetivos de Desarrollo Sostenible de la ONU, ya que un mejor acceso a servicios y oportunidades esenciales para todos los ciudadanos promueve un futuro más equitativo, sostenible y económicamente viable. Este análisis ayuda a identificar necesidades de infraestructura, servicios y planificación, priorizar intervenciones y definir políticas territoriales y de movilidad más efectivas.",
            style={'line-height': '1.2',
                   'font-size': '15px', 'margin-bottom': '16px'}
        ),
        html.P(
            "Con base en lo expuesto anteriormente, y en el contexto del TUMI Data Hub, se ha elaborado un tablero que se apoya en el modelo analítico creado por CAF y BID en el marco de OMU. Este modelo se utiliza para calcular los indicadores de accesibilidad urbana a centros de actividad y servicios básicos para diferentes niveles socioeconómicos.",
            style={'line-height': '1.2',
                   'font-size': '15px', 'margin-bottom': '30px'}
        ),
        html.H5(
            "Modelo Analítico",
            className="card-title",
            style={'margin-bottom': '16px',
                   'margin-top': '0',
                   'font-size': '24px'}
        ),
        html.P(
            "[1] Vanoli, C., & Anapolsky, S. (2023). Acceso a oportunidades en América Latina. Retrieved from https://cafscioteca.azurewebsites.net/handle/123456789/2003",
            style={'line-height': '1.2',
                   'font-size': '15px', 'margin-bottom': '30px', }
        ),
        html.H5(
            "Código",
            className="card-title",
            style={'margin-bottom': '16px',
                   'font-size': '24px'}
        ),
        html.A(
            "https://github.com/GuAI-Artificial-Intelligence/caf-accessibility-dashboard",
            style={'line-height': '1.2',
                   'font-size': '15px', },
            href="https://github.com/GuAI-Artificial-Intelligence/caf-accessibility-dashboard",
            target='_blank'
        ),
        html.Div(
            [
                html.P(
                    "Desarrollado por",
                    style={'line-height': '1.2',
                           'font-size': '15px', 'margin-top': '16px'}
                ),
                html.A(
                    "Guai",
                    href="https://www.guai.ai",
                    style={'margin-left': '8px'},
                    target='_blank'
                )
            ],
            style={"display": "flex",  "align-items": "center"}
        )


    ],
    style={'margin-left': '40px', 'margin-right': '40px'}
)

ACERCA_DE_BODY_METODOLOGIA = html.Div(
    children=[
        html.H5(
            "Fuentes de datos",
            className="card-title",
            style={'margin-bottom': '16px',
                   'font-size': '24px'}
        ),
        html.P(
            "Para el cálculo de accesibilidad urbana se requieren tres tipos de información: Orígenes, Destinos y tiempos/distancias.",
            style={'line-height': '1.2',
                   'font-size': '15px', 'margin-bottom': '15px'}
        ),
        html.H5(
            "Orígenes",
            className="card-title",
            style={'margin-bottom': '16px',
                   'font-size': '18px'}
        ),
        html.P(
            "Corresponde a las características de la población como ubicación de la vivienda, características de la vivienda (materiales, hacinamiento), características de la población (educación, nivel de ingresos), acceso a bienes, entre otras. Esta información usualmente se encuentra en los censos poblacionales. Para el desarrollo de este tablero se utilizaron:",
            style={'line-height': '1.2',
                   'font-size': '15px', 'margin-bottom': '10px'}
        ),
        html.Ul(
            [
                html.Li(
                    [
                        html.B("Bogotá: "),
                        "Censo Nacional de Población y Vivienda - CNPV - 2018 ",
                        html.A(
                            "(link de descarga)",
                            href="https://microdatos.dane.gov.co/index.php/catalog/643/get_microdata",
                            target='_blank'
                        ),
                    ]
                ),
                html.Li(
                    [
                        html.B("Cuenca: "),
                        "Censo de Población y Vivienda 2010 ",
                        html.A(
                            "(link de descarga)",
                            href="https://www.ecuadorencifras.gob.ec/base-de-datos-censo-de-poblacion-y-vivienda-2010-a-nivel-de-manzana/",
                            target='_blank'
                        ),
                    ]
                ),
            ],
            style={'margin-top': '0px'}
        ),

        html.H5(
            "Destinos",
            className="card-title",
            style={'margin-bottom': '16px',
                   'font-size': '18px'}
        ),
        html.Div(
            [
                html.P(
                    "En el modelo analítico creado por CAF y BID se denominan como atractores de viajes. Estos atractores están relacionados con los equipamientos a los cuales la población puede acceder desde su vivienda. Para el desarrollo de este tablero se utilizaron equipamientos de salud, educación y zonas verdes, los cuales están disponibles a través de la Interfaz para la Programación de Aplicaciones (API por sus siglas en inglés) de Open Street Maps (OSM en adelante).",
                    style={'line-height': '1.2',
                           'font-size': '15px', 'margin-bottom': '10px'}
                ),
                html.A(
                    "Open Street Maps",
                    href="https://wiki.openstreetmap.org/wiki/API_v0.6",
                    target='_blank'
                ),
            ],

        ),
        html.H5(
            "Tiempos/Distancias",
            className="card-title",
            style={'margin-bottom': '16px',
                   'font-size': '18px'}
        ),
        html.Div(
            [
                html.P(
                    "Para obtener el cálculo de accesibilidad se necesita estimar los tiempos y distancias de viaje desde la ubicación de la vivienda hasta el equipamiento de interés. Esta información debería tener en cuenta aspectos físicos de la infraestructura, como la malla vial y la red de transporte público. La forma más eficiente de obtener esta información es a través de la simulación de estos viajes a partir de las API públicas de las aplicaciones de ruteo de Google Maps y OSM.",
                    style={'line-height': '1.2',
                           'font-size': '15px', 'margin-bottom': '10px'}
                ),
                html.A(
                    "Google Maps",
                    href="https://mapsplatform.google.com/intl/es_ALL/products/#directions",
                    target='_blank'
                ),
            ],
            style={'margin-bottom': '30px'}

        ),

        html.P(
            "---",
            style={'line-height': '1.2',
                   'font-size': '15px', 'margin-bottom': '15px'}
        ),

        html.H5(
            "Cálculo de accesibilidad",
            className="card-title",
            style={'margin-bottom': '16px',
                   'font-size': '24px'}
        ),
        html.P(
            "El cálculo de accesibilidad se realiza a partir de los siguientes pasos:",
            style={'line-height': '1.2',
                   'font-size': '15px', 'margin-bottom': '8px', }
        ),
        html.Ol(
            [
                html.Li(
                    [
                        "Procesamiento de la información:",
                        html.Ul(
                            [
                                html.Li(
                                    "Orígenes: homogeneización de la cartografía censal a partir de la creación de hexágonos de igual tamaño y la posterior estimación de Población y Nivel Socioeconómico."),
                                html.Li(
                                    "Destinos: obtención de la ubicación geográfica (Longitud, Latitud) de los equipamientos de interés."),
                            ]
                        )
                    ]
                ),
                html.Li(
                    [
                        "Simulación de viajes:",
                        html.Ul(
                            [
                                html.Li(
                                    "Para el cálculo de distancias se utiliza la API de OSM."),
                                html.Li(
                                    "Para la estimación de los tiempos de viaje en distintos modos de transporte se utilizar la API de Google Maps"),
                            ]
                        )

                    ]
                ),
                html.Li(
                    [
                        "Cálculo del indicador de accesibilidad: a partir de los datos generados en la simulación se procede a:",
                        html.Ul(
                            [
                                html.Li(
                                    "Cálculo de indicadores de congestión y accesibilidad a equipamientos."),
                                html.Li(
                                    "Cálculo de clusters de accesibilidad a partir de un proceso de clusterización (k-means) utilizando indicadores como distancia de acceso caminando al transporte público, distancia a los establecimientos principales (educación primaria y atención primaria de salud), cantidad de estos establecimientos en 2 km y tiempos de viaje al área central. Como resultado cada hexágono es asignado a una clase: Alta, Media Alta, Media Baja y Baja."),
                            ]
                        )
                    ]
                ),
            ],
            style={'margin-top': '0px', 'margin-bottom': '30px'}
        ),
        html.P(
            "---",
            style={'line-height': '1.2',
                   'font-size': '15px', 'margin-bottom': '15px'}
        ),
        html.H5(
            "Cómo interpretar los resultados",
            className="card-title",
            style={'margin-bottom': '16px',
                   'font-size': '24px'}
        ),
        html.Ul(
            [
                html.Li(
                    [
                        html.B("Alta accesibilidad: "),
                        "quienes viven aquí se encuentran a aproximadamente 18 minutos en bus del área central de la ciudad, tienen el transporte público a 463 metros en mediana, y tienen una oferta variada de equipamientos de educación y salud (aproximadamente 29 y 2 respectivamente).",
                    ]
                ),
                html.Li(
                    [
                        html.B("Media Alta accesibilidad: "),
                        "quienes viven aquí se encuentran a aproximadamente 41 minutos en bus del área central de la ciudad, tienen el transporte público a 386 metros en mediana, y tienen mayor cantidad de equipamientos de educación y salud (aproximadamente 56 y 4 respectivamente).",
                    ]
                ),
                html.Li(
                    [
                        html.B("Media Baja accesibilidad: "),
                        "quienes viven aquí se encuentran a aproximadamente 40 minutos en bus del área central de la ciudad, tienen el transporte público a 430 metros en mediana, y tienen una oferta variada de equipamientos de educación y salud (aproximadamente 30 y 2 respectivamente).",
                    ]
                ),
                html.Li(
                    [
                        html.B("Baja accesibilidad: "),
                        "quienes viven aquí se encuentran a aproximadamente 47 minutos en bus del área central de la ciudad, tienen el transporte público a 1038 metros en mediana, y no tienen buena oferta de equipamientos de educación y salud (aproximadamente 1 y 0 respectivamente).",
                    ]
                )
            ],
            style={'margin-top': '0px'}
        ),
        html.H5(
            "Ventajas y Limitaciones",
            className="card-title",
            style={'margin-bottom': '16px',
                   'font-size': '24px'}
        ),
        html.P(
            "Con la implementación de este tablero a partir del modelo analitico desarrollado por CAF y BID se tienen las siguientes ventajas:",
            style={'line-height': '1.2',
                   'font-size': '15px', 'margin-bottom': '15px', }
        ),
        html.Ul(
            [
                html.Li(
                    [
                        "Se utilizan datos que están disponibles a nivel país (censos de población y vivienda).",
                    ]
                ),
                html.Li(
                    [
                        "Se tiene un nivel de granularidad suficiente para mejorar la toma de decisiones.",
                    ]
                ),
                html.Li(
                    [
                        "Se puede tener la información a la mano .",
                    ]
                ),
                html.Li(
                    [
                        "Se puede hacer la implementación en otras ciudades.",
                    ]
                )
            ],
            style={'margin-top': '0px'}
        ),



        html.P(
            "Sin embargo, es importante resaltar sus limitaciones para ver el alcance de las decisiones:",
            style={'line-height': '1.2',
                   'font-size': '15px', 'margin-bottom': '15px', }
        ),
        html.Ul(
            [
                html.Li(
                    [
                        "La información puede que no sea actualizada. Por ejemplo, el último censo de ecuador fue en 2010.",
                    ]
                ),
                html.Li(
                    [
                        "La simulación de los viajes está sujeta a la calidad de datos de los proveedores Google Maps y OSM.",
                    ]
                ),
            ],
            style={'margin-top': '0px'}
        ),




    ],
    style={'margin-left': '40px', 'margin-right': '40px'}
)


ESPACIO_CAF_BODY_METODOLOGIA = html.Div(
    children=[
        #     html.H5(
        #         "Fuentes de datos",
        #         className="card-title",
        #         style={'margin-bottom': '16px',
        #                'font-size': '24px'}
        #     ),
        html.P(
            "A través del uso y valorización de los datos de movilidad, CAF y TUMI se unieron para implementar el Proyecto “Mobility Data Hub - Datos abiertos para una movilidad sostenible e inclusiva en América Latina”, con el fin de sembrar las semillas de la transformación digital de la movilidad urbana en la región.",
            style={'line-height': '1.2',
                   'font-size': '15px', 'margin-bottom': '30px'}
        ),
        html.P(
            "CAF y TUMI, junto a sus socios de ejecución técnica NUMO (New Urban Mobility Initiative) han definido conceptualmente el proyecto Mobility Data Hub, el cual se ejecutará a través de tres componentes: Mobility Data Hub, pilotos en ciudades e investigación académica. Esta aplicación es parte del primer componente del proyecto.",
            style={'line-height': '1.2',
                   'font-size': '15px', 'margin-bottom': '30px'}
        ),

    ],
    style={'margin-left': '40px', 'margin-right': '40px'}
)


NONE_TRACE_NAME = 'NONE'
MAP_TRACE_NAME = 'MAP'
HOSPITAL_TRACE_NAME = 'HOSP'
ESPACIOS_VERDES_TRACE_NAME = 'ESP_VERD'
ATENCION_PRIMARIA_TRACE_NAME = 'ATENCION_PRIMARIA'

EARLY_EDUCATION_TRACENAME = 'EDUCACION_INICIAL'
PRIMARY_EDUCATION_TRACENAME = 'EDUCACION_PRIMARIA'
SECONDARY_EDUCATION_TRACENAME = 'EDUCACION_SECUNDARIA'


VARIABLE_OPTIONS_CAR = [
    {'label': 'Salud (Atención primaria): Distancia (km)',
     'value': 'avg_distance_primary_health_care_driving_car'},
    {'label': 'Salud (Atención primaria): Tiempo (min)',
     'value': 'avg_duration_primary_health_care_driving_car'},
    {'label': 'Salud (Hospitales): Distancia (km)',
     'value': 'avg_distance_hospitals_driving_car'},
    {'label': 'Salud (Hospitales): Tiempo (min)',
     'value': 'avg_duration_hospitals_driving_car'},
    {'label': 'Educación (Inicial): Distancia (km)',
     'value': 'avg_distance_early_education_driving_car'},
    {'label': 'Educación (Inicial): Tiempo (min)',
     'value': 'avg_duration_early_education_driving_car'},
    {'label': 'Educación (Primaria): Distancia (km)',
     'value': 'avg_distance_primary_education_driving_car'},
    {'label': 'Educación (Primaria): Tiempo (min)',
     'value': 'avg_duration_primary_education_driving_car'},
    {'label': 'Educación (Secundaria): Distancia (km)',
     'value': 'avg_distance_secondary_education_driving_car'},
    {'label': 'Educación (Secundaria): Tiempo (min)',
     'value': 'avg_duration_secondary_education_driving_car'},
]

VARIABLE_OPTIONS_BYCICLE = [
    {'label': 'Salud (Atención primaria): Distancia (km)',
     'value': 'avg_distance_primary_health_care_cycling_regular'},
    {'label': 'Salud (Atención primaria): Tiempo (min)',
     'value': 'avg_duration_primary_health_care_cycling_regular'},
    {'label': 'Salud (Hospitales): Distancia (km)',
     'value': 'avg_distance_hospitals_cycling_regular'},
    {'label': 'Salud (Hospitales): Tiempo (min)',
     'value': 'avg_duration_hospitals_cycling_regular'},
    {'label': 'Educación (Inicial): Distancia (km)',
     'value': 'avg_distance_early_education_cycling_regular'},
    {'label': 'Educación (Inicial): Tiempo (min)',
     'value': 'avg_duration_early_education_cycling_regular'},
    {'label': 'Educación (Primaria): Distancia (km)',
     'value': 'avg_distance_primary_education_cycling_regular'},
    {'label': 'Educación (Primaria): Tiempo (min)',
     'value': 'avg_duration_primary_education_cycling_regular'},
    {'label': 'Educación (Secundaria): Distancia (km)',
     'value': 'avg_distance_secondary_education_cycling_regular'},
    {'label': 'Educación (Secundaria): Tiempo (min)',
     'value': 'avg_duration_secondary_education_cycling_regular'},
]

VARIABLE_OPTIONS_FOOT = [
    {'label': 'Salud (Atención primaria): Distancia (km)',
     'value': 'avg_distance_primary_health_care_foot_walking'},
    {'label': 'Salud (Atención primaria): Tiempo (min)',
     'value': 'avg_duration_primary_health_care_foot_walking'},
    {'label': 'Salud (Hospitales): Distancia (km)',
     'value': 'avg_distance_hospitals_foot_walking'},
    {'label': 'Salud (Hospitales): Tiempo (min)',
     'value': 'avg_duration_hospitals_foot_walking'},
    {'label': 'Educación (Inicial): Distancia (km)',
     'value': 'avg_distance_early_education_foot_walking'},
    {'label': 'Educación (Inicial): Tiempo (min)',
     'value': 'avg_duration_early_education_foot_walking'},
    {'label': 'Educación (Primaria): Distancia (km)',
     'value': 'avg_distance_primary_education_foot_walking'},
    {'label': 'Educación (Primaria): Tiempo (min)',
     'value': 'avg_duration_primary_education_foot_walking'},
    {'label': 'Educación (Secundaria): Distancia (km)',
     'value': 'avg_distance_secondary_education_foot_walking'},
    {'label': 'Educación (Secundaria): Tiempo (min)',
     'value': 'avg_duration_secondary_education_foot_walking'},
]
