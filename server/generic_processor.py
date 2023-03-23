import os


class GenericProcessor:
    @staticmethod
    def html_template_returner(content):
        return """
<html>
<body>
<style type="text/css" media="screen">
table, th, td {{
border: 1px solid black;
text-align: center;
}}
</style>
{}
<p style="margin-bottom:0;">Thanks,</p>
<p style="margin : 0; padding-top:0;">Easy Pay</p>
</body>
</html>
        """.format(
            content
        )