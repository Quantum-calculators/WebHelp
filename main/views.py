from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .forms import LinkForm
from .parser import Parser
from .Classifier.process import topic_determinant


class MainView(View):
    template_name = "main/index.html"

    def get(self, request):
        form = LinkForm()
        return render(request, "main/index.html", {"form": form})

    def post(self, request):
        data = request.POST
        form = LinkForm()
        # if request.is_ajax():
        if data["link"]:
            link = data["link"]
            parsed_data = Parser.parse(link)
            theme = topic_determinant(
                list_of_words=parsed_data[1], exit_code=parsed_data[2]
            )
            if theme[0] != 0:
                if theme[0] != 1:
                    category_name = (
                        "Could not access the resource. Status code of the specified site: "
                        + str(theme[0])
                    )
                    theme_name = ""
                else:
                    category_name = "Could not access the resource."
                    theme_name = ""
            else:
                category_name = theme[2]
                theme_name = theme[1]
            response = {"category": category_name, "theme": theme_name, "link": link}
            return JsonResponse(response, status=200)
        else:
            errors = "The url was not specified"
            return JsonResponse({"errors": errors}, status=400)


def check_domain(request):
    link = request.GET.get("domain")
    parsed_data = Parser.parse(link)
    theme = topic_determinant(list_of_words=parsed_data[1], exit_code=parsed_data[2])
    if theme[0] != 0:
        if theme[0] != 1:
            category_name = (
                "Could not access the resource. Status code of the specified site: "
                + str(theme[0])
            )
            theme_name = "Parse Error"
        else:
            category_name = "Could not access the resource."
            theme_name = f"Status code: {theme[0]}"
    else:
        category_name = str(theme[1])
        theme_name = str(theme[1])
    response = {"category": category_name, "theme": theme_name, "link": link}
    return JsonResponse(response)
    # return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
