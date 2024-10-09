import taipy.gui.builder as tgb

from pages.sidebar import sidebar_partial

layout_columns = "2 8"

with tgb.Page() as page:
    with tgb.layout(columns=layout_columns):
        with tgb.part("sidebar"):
            sidebar_partial()

        with tgb.part():
            tgb.navbar()
            tgb.html("h2", "About Me")
            tgb.html(
                "p",
                "Currently I am working in a state-owned exchange group as Data Director, I live in Shanghai and studied in Germany and the US.",
            )
            tgb.html(
                "p",
                "Over the course of past ten plus years, I have acquired both academic and practical experience as a versatile individual, excelling as a Software Engineer with a strong proficiency in Python and as a skilled Data Scientist with expertise in Governance."
            )
            tgb.html(
                "p",
                "My language abilities are a significant asset, with fluency in Professional English and Competent German."
            )
            tgb.html(
                "p",
                "Moreover, I have nurtured my expertise through hands-on experiences in a diverse range of fields, including Product Development, Software Engineering, Data Management, Machine Learning and Large Language Models."
            )   
            tgb.html(
                "p",
                "These cumulative experiences have shaped me into a well-rounded professional, primed to embrace new challenges and deliver impactful contributions to any data freelancing endeavor."
            )
            
            tgb.html("h3", "What I'm specialized at")
            with tgb.layout(columns="1 1"):
                with tgb.part("card"):
                    tgb.html("h4", "Software Engineer", className="h4-height")
                    tgb.html(
                        "p",
                        """
                        I specialize in leading the development of innovative solutions using Django and Taipy, 
                        combining robust back-end frameworks with intuitive, data-driven front-end interfaces.
                        """
                    )
                with tgb.part("card"):
                    tgb.html("h4", "Data Management", className="h4-height")
                    tgb.html(
                        "p",
                        """
                        As a Certified Data Management Professional, 
                        I specialize in data modeling using Pydantic, graph modeling with Neo4j, 
                        and data integration with tools like Airbyte.
                        """
                    )
            tgb.html("br")

            with tgb.layout(columns="1 1"):
                with tgb.part("card"):
                    tgb.html("h4", "LLM Applications", className="h4-height")
                    tgb.html(
                        "p",
                        """
                        I design and implement AI-driven solutions with LangChain, 
                        enhancing business performance and user experience.
                        """
                    )
                with tgb.part("card"):
                    tgb.html("h4", "Data Analysis", className="h4-height")
                    tgb.html(
                        "p",
                        """
                        I use Polars to efficiently process and analyze large datasets, enabling faster computations and insightful results. 
                        """
                    )

            tgb.html("h3", "Testimonials")

            # Note: Ebbelaar and Schwabe
            with tgb.layout(columns="1 1"):
                with tgb.part("card"):
                    tgb.html(
                        "div", 
                        """
                            <img src="https://assets.skool.com/f/084d824e02714b77b4f1fda3613e92b9/b2120f46d3014b8f9638d98e4699cdb1691693cb54d840c79dc58f5de84c05f9" 
                                style="width:60px; height:60px; margin-right:15px;">
                            </img>
                            <h4>Dave Ebbelaar</h4>                        
                        """,
                        className="image-text-container"
                    )

                    tgb.html(
                        "p",
                        """
                        Dave founded the company Datalumina in 2022.
                        The company now focuses on building intelligent, data-centric solutions and helping businesses effectively implement 
                        and leverage AI to drive innovation and growth.
                        """
                    )
                    tgb.html(
                        "p",
                        "<strong>I joined his data freelancing program in 2024.</strong>"
                    )
                        
                with tgb.part("card"):
                    tgb.html(
                        "div", 
                        """
                            <img src="https://media.licdn.com/dms/image/v2/D4E03AQE2kIhGn_itew/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1688821634455?e=2147483647&v=beta&t=a-sL6pZuIBbn2BTTJNkMSq9-NnLcLE-KibzefFfvOpM" 
                                style="width:60px; height:60px; margin-right:15px;">
                            </img>
                            <h4>Lars Schwabe</h4>                        
                        """,
                        className="image-text-container"
                    )
                    
                    tgb.html(
                        "p",
                        """
                        Lars was a Professor of Adaptive and Regenerative Software Systems at the University of Rostock.
                        Since February 2022, he has taken over the leadership of Digital Strategy department at Lufthansa Industry Solutions.
                        """
                    )
                    tgb.html(
                        "p",
                        "<strong>I was his doctoral student from 2010 to 2015.</strong>"
                    )

            # Note: blank separator                    
            tgb.html(
                "p",
                ""
            )

            # Note: Hans-Jörg Schulz and Plotkin                    
            with tgb.layout(columns="1 1"):
                with tgb.part("card"):
                    tgb.html(
                        "div", 
                        """
                            <img src="https://media.licdn.com/dms/image/v2/C5603AQFhtgdzhWPo2Q/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1524573886871?e=1732752000&v=beta&t=_G0CeFQnSx2-cbUurIdRtSHCXYES6WmatpT2ctgSQlM" 
                                style="width:60px; height:60px; margin-right:15px;">
                            </img>
                            <h4>Hans-Jörg Schulz</h4>                        
                        """,
                        className="image-text-container"
                    )

                    tgb.html(
                        "p",
                        """
                        Hans-Jörg is an associate professor at the Department of Computer Science at Aarhus University in Denmark.
                        """
                    )
                    tgb.html(
                        "p",
                        "<strong>We collaborated on multi-disciplinary projects.</strong>"
                    )
                        
                with tgb.part("card"):
                    tgb.html(
                        "div", 
                        """
                            <img src="https://media.licdn.com/dms/image/v2/C5103AQE1APfhIbh8LA/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1516242274465?e=1732752000&v=beta&t=jVPnhTQ1_jJgoLGucKhoSDDqMsp8b6Pyzov7dcA9X24" 
                                style="width:60px; height:60px; margin-right:15px;">
                            </img>
                            <h4>Joshua L. Plotkin</h4>                        
                        """,
                        className="image-text-container"
                    )
                    
                    tgb.html(
                        "p",
                        """
                        Joshua is an associate professor at the Department of Neurobiology at Stony Brook University in United States.
                        """
                    )
                    tgb.html(
                        "p",
                        "<strong>We published Computational Neuroscience papers.</strong>"
                    )


