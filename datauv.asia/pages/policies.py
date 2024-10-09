import taipy.gui.builder as tgb
from pages.sidebar import sidebar_partial

layout_columns = "2 8"  # Define your layout columns ratio

with tgb.Page() as page:
    with tgb.layout(columns=layout_columns):
        with tgb.part("sidebar"):
            sidebar_partial()  # Render the sidebar content

        with tgb.part():
            tgb.navbar()  # Render the navbar
            tgb.html("h1", "Fulfillment Policies")

            tgb.html("ul", children=[
                tgb.html("li", "Refund Policy"),
                tgb.html(
                    "p",
                    "Customers can request a refund within 30 days of purchase for services that have not yet commenced. If a service has already started, refunds are evaluated on a case-by-case basis. Please contact our support team for more information."
                ),

                tgb.html("li", "Delivery Policy"),
                tgb.html(
                    "p",
                    "For digital services, once payment is confirmed, we initiate the project immediately or as per the mutually agreed timeline. Delivery timelines for reports and other deliverables will be communicated during the project scoping stage. For software development projects, delivery milestones are set during the project discussion phase."
                ),

                tgb.html("li", "Return Policy"),
                tgb.html(
                    "p",
                    "As our services are digital and tailored to each customer’s needs, returns are not applicable. However, we strive to ensure that our services meet your expectations. If you have concerns, please contact us to discuss the resolution."
                ),

                tgb.html("li", "Cancellation Policy"),
                tgb.html(
                    "p",
                    "Customers can cancel their subscription-based services at any time before the next billing cycle. For project-based services, cancellations must be requested within the first 14 days after project commencement for a partial refund. No refunds are given for cancellations after the 14-day period."
                ),
            ])
