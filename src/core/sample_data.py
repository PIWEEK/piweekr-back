from sampledata.helper import SampleData

import arrow
import random
import uuid

from .users import user_entities
from .ideas import idea_entities
from .projects import project_entities

from services.repository.sql import repo
from services.repository.sql.users import user_repository
from services.repository.sql.ideas import idea_repository
from services.repository.sql.projects import project_repository


sample_colors = ["#FC8EAC", "#A5694F", "#002e33", "#67CF00", "#71A6D2", "#FFF8E7", "#4B0082", "#007000",
 		 "#40826D", "#708090", "#761CEC", "#0F0F0F", "#D70A53", "#CC0000", "#FFCC00", "#FFFF00",
		 "#C0FF33", "#B6DA55", "#2099DB"]

sample_technologies = ["python", "groovy", "c", "html", "css", "angualr", "cloujure", "cloujurescript", "IoT",
                       "music", "UX", "Design", "SASS", "CSS", "HTML", "PostCSS"]

sample_emojis = ["smile", "thumbsdown", "thumbsup", "poo", "confused", "dancer", "beer"]


sample_logos = ["http://createfunnylogo.com/blazed/MetanOR.jpg",
                "http://createfunnylogo.com/logo/techcrunch/Virtual%20Gym.jpg",
                "http://createfunnylogo.com/logo/flickr/PiWeekr.jpg"]

class SampleData():
    sd = SampleData(seed=1234567890)

    def run(self):
        repo.truncate_all_tables()

        self.user_ids = []
        self.piweek_ids = []
        self.idea_ids = []
        self.project_ids = []

        print("Generating sample data...")
        self.make_users()
        self.make_ideas()
        self.make_projects()
        print("Done.")

    def make_users(self):
        from tools.password import generate_hash

        for i in range(10):
            username = "user-{}".format(i + 1)
            user = user_entities.User(
                username=username,
                password=generate_hash("123123"),
                full_name=self.sd.fullname(locale='us'),
                email=self.sd.word() + '@piweekr.org',
                avatar = {
                    "head": self.sd.int(1, 23),
                    "body": self.sd.int(1, 23),
                    "legs": self.sd.int(1, 10),
                    "background": self.sd.choice(sample_colors),
                }
            )
            user = user_repository.create(user)
            self.user_ids.append(user.id)
            print("User '{}' created.".format(user.email))

    def make_ideas(self):
        for i in range(50):
            idea = idea_entities.Idea(
                uuid=uuid.uuid4().hex,
                is_active=True,
                title=self.sd.words(1, 4).capitalize(),
                description=self.sd.paragraphs(1, 3),
                owner_id=random.choice(self.user_ids),
                created_at=arrow.get(self.sd.past_datetime()),
                is_public=self.sd.boolean(),
                forked_from=random.choice(self.idea_ids) if self.idea_ids and self.sd.int(1, 8) == 1 else None,
                comments_count=self.sd.int(0, 10),
                reactions_counts={self.sd.choice(sample_emojis): self.sd.int(1, 10) for j in range(self.sd.int(0, 3))},
            )
            idea = idea_repository.create(idea)
            self.idea_ids.append(idea.id)
            print("Idea '{}' created.".format(idea.uuid))

            for j in range(idea.comments_count):
                comment = idea_entities.IdeaComment(
                    uuid=uuid.uuid4().hex,
                    content=self.sd.long_sentence(),
                    owner_id=random.choice(self.user_ids),
                    idea_id=idea.id,
                    created_at=arrow.get(self.sd.past_datetime()),
                )
                idea_repository.create_comment(comment)
                print("Comment '{}' created.".format(comment.uuid))

            if not idea.is_public:
                if self.sd.int(1, 3) == 1:
                    excluded_ids = [idea.owner_id]
                    for j in range(self.sd.int(1, 4)):
                        while True:
                            user_id = random.choice(self.user_ids)
                            if not user_id in excluded_ids:
                                excluded_ids.append(user_id)
                                break
                        invited = idea_entities.IdeaInvited(
                            idea_id=idea.id,
                            user_id=user_id,
                        )
                        invited = idea_repository.create_invited(invited)

    def make_projects(self):
        for i in range(20):

            if self.sd.int(1, 5) == 1:
                idea_from = None
            else:
                ideas = idea_repository.list() # This only retrieves active ideas
                idea_from = random.choice(ideas)
                idea_from.deactivate()
                idea_repository.update(idea_from)

            project = project_entities.Project(
                uuid=uuid.uuid4().hex,
                title=self.sd.words(1, 4).capitalize(),
                description=self.sd.paragraphs(1, 3),
                technologies=[self.sd.choice(sample_technologies) for i in range(self.sd.int(0, 5))],
                needs=self.sd.paragraphs(1, 2),
                logo=self.sd.choice(sample_logos),
                piweek_id=1, # TODO
                idea_from_id=idea_from.id if idea_from else None,
                owner_id=random.choice(self.user_ids),
                created_at=arrow.get(self.sd.past_datetime()),
                comments_count=self.sd.int(0, 10),
                reactions_counts={self.sd.choice(sample_emojis): self.sd.int(1, 10) for j in range(self.sd.int(0, 3))},
            )
            project = project_repository.create(project)
            self.project_ids.append(project.id)
            print("Project '{}' created.".format(project.uuid))

            for j in range(project.comments_count):
                comment = project_entities.ProjectComment(
                    uuid=uuid.uuid4().hex,
                    content=self.sd.long_sentence(),
                    owner_id=random.choice(self.user_ids),
                    project_id=project.id,
                    created_at=arrow.get(self.sd.past_datetime()),
                )
                project_repository.create_comment(comment)
                print("Comment '{}' created.".format(comment.uuid))

