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
SCATTER_ID = "my-scatter"
MAP_ID = 'my-map'
CITY_SELECTOR = 'my-city-selector'
ACCESIBILITY_SELECTOR = 'my-accesibility-selector'
CATEGORY_SELECTOR = 'my-category-selector'
VARIABLE_SELECTOR = 'my-variable-selector'
INFRA_CHECKLIST_ID = 'infra-checklist'

CATEGORICAL_VARIABLES = ['IndiAcce_1', 'NSE_5']
NON_CATEGORICAL_VARIABLES = ['Poblacion']

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
    orientation='v',
    thickness=0.04,
    y=0.32,
    x=0.909,
    len=0.04,
    tickfont=dict(color="#323232", size=1)
    
)

HIDDEN_COLORSCALE = ['#000000','#000000','#000000','#000000']

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
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum",
            style={'line-height': '1.2',
                   'font-size': '15px', 'margin-bottom': '30px'}
        ),
        html.H5(
            "Cálculo de accesibilidad",
            className="card-title",
            style={'margin-bottom': '16px',
                   'font-size': '24px'}
        ),
        html.P(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum",
            style={'line-height': '1.2',
                   'font-size': '15px', 'margin-bottom': '30px', }
        ),
        html.H5(
            "Cómo interpretar los resultados",
            className="card-title",
            style={'margin-bottom': '16px',
                   'font-size': '24px'}
        ),
        html.P(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum",
            style={'line-height': '1.2',
                   'font-size': '15px', 'margin-bottom': '30px', }
        ),
        html.H5(
            "Limitaciones",
            className="card-title",
            style={'margin-bottom': '16px',
                   'font-size': '24px'}
        ),
        html.P(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum",
            style={'line-height': '1.2',
                   'font-size': '15px', 'margin-bottom': '30px', }
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


MAP_TRACE_NAME = 'MAP'
HOSPITAL_TRACE_NAME = 'HOSP'
ESPACIOS_VERDES_TRACE_NAME = 'ESP_VERD'