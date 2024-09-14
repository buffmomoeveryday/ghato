# import random

# from django.urls import reverse_lazy
# from django_components import component
# from django_components import types as t
# from sourcetypes import django_html


# @component.register("button")
# class Button(component.Component):

#     def get_context_data(
#         self,
#         label,
#         disabled=False,
#         type: str = None,
#         id=None,
#     ):

#         if id is None:
#             id = label + str(random.randint(1, 900))

#         if type is None:
#             return {
#                 "id": id,
#                 "label": label,
#                 "disabled": disabled,
#             }

#         return {
#             "id": id,
#             "label": label,
#             "disabled": disabled,
#             "type": type,
#         }

#     template: django_html = """
#     <button type="submit" id="{{ id }}"
#      data-loading-class="bg-gray-100 opacity-80"
#     class="w-full inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
#     {% if disabled %}disabled{% endif %}>
#     {{label}}
#     </button>

#     """


# @component.register("input")
# class Input(component.Component):

#     def get_context_data(
#         self,
#         id,
#         label,
#         name,
#         placeholder: str = "",
#         required: bool = False,
#         type: str = "text",
#         value: str = None,
#     ):

#         return {
#             "id": id,
#             "label": label,
#             "type": type,
#             "name": name,
#             "placeholder": placeholder,
#             "required": required,
#             "value": value,
#         }

#     template: t.django_html = """
#     <label for="{{ id }}" class="block text-sm font-medium text-gray-700">{{ label }}</label>
#             <input type="{{ type }}" id="{{ id }}" name="{{ name }}"
#             {% if placeholder %}
#                 placeholder="{{placeholder}}"
#             {% endif %}
#             {% if required %}
#                 required
#             {% endif %}
#             {% if value %}
#             value="{{value}}"
#             {% endif %}

#                 class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">

#                 """


# @component.register("link")
# class Link(component.Component):
#     def get_context_data(
#         self, label: str, url: str = None, id: str = None, boost=False, **kwargs
#     ):

#         if id is None:
#             id = f"{label.lower()}-{random.randint(1,9)}"

#         context = {
#             "id": id,
#             "label": label,
#             "url": reverse_lazy(url),
#             "boost": boost,
#         }

#         return context

#     template: t.django_html = """
#                     <a
#                     id={{id}}
#                     {% if boost %}
#                         hx-boost="true"
#                     {% else %}
#                         hx-boost="false"
#                     {% endif %}
#                        href="{{url}}"
#                        class="text-indigo-600 hover:underline focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
#                         {{label}}
#                     </a>
#                 """


# @component.register("modal")
# class Modal(component.Component):
#     def get_context_data(self, label, modal, header, url=None, unicorn_url=None):
#         context = {
#             "label": label,
#             "modal": modal,
#             "header": header,
#             "url": reverse_lazy(url) if url else None,
#             "unicorn_url": unicorn_url,
#         }
#         return context

#     template: django_html = """
#     <button data-modal-target="{{modal}}" data-modal-toggle="{{modal}}"
#         class="block text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
#         type="button">
#         {{label}}
#     </button>

#     <!-- Main modal -->
#     <div id="{{modal}}" tabindex="-1" aria-hidden="true" class="hidden overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full">
#         <div class="relative p-4 w-full max-w-md max-h-full">
#             <!-- Modal content -->
#             <div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
#                 <!-- Modal header -->
#                 <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600">
#                     <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
#                         {{header}}
#                     </h3>
#                     <button type="button" class="end-2.5 text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white" data-modal-hide="{{modal}}">
#                         <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
#                             <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
#                         </svg>
#                         <span class="sr-only">Close modal</span>
#                     </button>
#                 </div>
#                 <!-- Modal body -->
#                 <div class="p-4 md:p-5">
#                     <form class="space-y-4"
#                     {% if unicorn_url %}
#                         u:submit.prevent="{{unicorn_url}}"
#                     {% elif url %}
#                         action="{{url}}" method="post"
#                     {% endif %}>
#                         {% csrf_token %}
#                         {% slot "form" %}
#                         {% endslot %}
#                         <button type="submit" class="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
#                             Save
#                         </button>
#                     </form>
#                 </div>
#             </div>
#         </div>
#     </div>
#     """
