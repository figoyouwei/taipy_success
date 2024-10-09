import taipy.gui.builder as tgb
from pages.sidebar import sidebar_partial

layout_columns = "2 8"  # Define your layout columns ratio

with tgb.Page() as page:
    with tgb.layout(columns=layout_columns):
        with tgb.part("sidebar"):
            sidebar_partial()  # Render the sidebar content

        with tgb.part():
            tgb.navbar()  # Render the navbar
            tgb.html("h2", "Service Description")

            tgb.html("ul", children=[
                # Software Development
                tgb.html("li", "Software Development"),
                tgb.html(
                    "p", 
                    "We build robust, scalable software applications customized to your specific business needs. Whether you need a web application, custom tools, or full-stack solutions, we ensure top-quality performance, security, and user experience."
                ),

                # Data Management
                tgb.html("li", "Data Management"),
                tgb.html(
                    "p", 
                    "Our data management services ensure that your data is organized, secure, and accessible. We offer comprehensive data integration solutions, database design, and optimization, along with secure data storage and backup strategies."
                ),

                # LLM Applications
                tgb.html("li", "LLM Applications"),
                tgb.html(
                    "p", 
                    "Harness the power of AI with our LLM solutions, including chatbots, text analysis, and natural language processing applications. We help businesses automate tasks, enhance customer engagement, and derive actionable insights from vast amounts of textual data."
                ),

                # Data Analysis
                tgb.html("li", "Data Analysis"),
                tgb.html(
                    "p", 
                    "Our data analysis services provide you with valuable insights to drive business decisions. We specialize in data visualization, statistical modeling, and advanced analytics to transform raw data into actionable strategies that fuel growth."
                ),
            ])

            tgb.html(
                "p", 
                "Each service we offer is designed with precision and care, ensuring a clear understanding of your project requirements. Whether you need a long-term project or a short-term consultation, we set transparent goals and deliver measurable results.",
                style="color: orange;"
            )
