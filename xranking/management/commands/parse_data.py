from django.core.management.base import BaseCommand
from xranking.models import Project, Query, ProjectQuery, ProjectResult, SearchResult
import os
import re
from urllib.parse import urlparse


class Command(BaseCommand):
    help = 'Parse data from folders and populate database tables.'

    def add_arguments(self, parser):
        parser.add_argument('--positions_folder', type=str, help='Path to the positions folder.', default='')
        parser.add_argument('--results_folder', type=str, help='Path to the results folder.', default='')

    def handle(self, *args, **kwargs):
        positions_folder_path = kwargs['positions_folder']
        results_folder_path = kwargs['results_folder']

        if positions_folder_path:
            self.process_positions_folder(positions_folder_path)

        if results_folder_path:
            self.process_results_folder(results_folder_path)

    def process_positions_folder(self, positions_folder_path):
        for folder_name in os.listdir(positions_folder_path):
            folder_path = os.path.join(positions_folder_path, folder_name)

            if os.path.isdir(folder_path):
                project, created = Project.objects.get_or_create(domain=folder_name)

                for file_name in os.listdir(folder_path):
                    if file_name.endswith('.txt') and re.match(r'\d{4}-\d{2}-\d{2}\.txt', file_name):
                        file_path = os.path.join(folder_path, file_name)

                        with open(file_path, 'r', encoding='utf-8') as file:
                            lines = file.readlines()

                            for line in lines:
                                parts = line.strip().split(';')

                                if len(parts) >= 2:
                                    query_text, region = parts[0], parts[1]
                                    query = Query.objects.create(query=query_text, region=region)
                                    project_query = ProjectQuery.objects.create(project=project, query=query)

    def process_results_folder(self, results_folder_path):
        for folder_name in os.listdir(results_folder_path):
            folder_path = os.path.join(results_folder_path, folder_name)

            pattern = r'^(.*)_([0-9]+)$'
            match = re.match(pattern, folder_name)

            if match:
                query, region = match.group(1), int(match.group(2))
                query = Query.objects.filter(query=query, region=region).first()

                if query and os.path.isdir(folder_path):
                    self.process_result_files(folder_path, query)

    def process_result_files(self, folder_path, query):
        for file_name in os.listdir(folder_path):
            date_pattern = r'(\d{4}-\d{2}-\d{2})\.txt'
            match = re.search(date_pattern, file_name)

            if match:
                date = match.group(1)
                file_path = os.path.join(folder_path, file_name)

                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                    for line in lines:
                        pattern = r'^(\d+)\.\s*(https?://\S+)'
                        match = re.match(pattern, line)

                        if match:
                            position, url = int(match.group(1)), match.group(2)
                            parsed_url = urlparse(url)
                            domain = parsed_url.netloc

                            SearchResult.objects.create(
                                query=query,
                                domain=domain,
                                date=date,
                                url=url,
                                position=position
                            )

                            ProjectResult.objects.create(
                                project=query.projectquery.project,
                                query=query,
                                date=date,
                                url=url,
                                position=position
                            )
