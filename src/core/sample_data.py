from sampledata.helper import SampleData

import arrow
import random
import uuid

from .users import user_entities
from .ideas import idea_entities

from services.repository.sql import repo
from services.repository.sql.users import user_repository
from services.repository.sql.ideas import idea_repository


sample_colors = ["#FC8EAC", "#A5694F", "#002e33", "#67CF00", "#71A6D2", "#FFF8E7", "#4B0082", "#007000",
 		 "#40826D", "#708090", "#761CEC", "#0F0F0F", "#D70A53", "#CC0000", "#FFCC00", "#FFFF00",
		 "#C0FF33", "#B6DA55", "#2099DB"]

class SampleData():
    sd = SampleData(seed=1234567890)

    def run(self):
        repo.truncate_all_tables()

        self.user_ids = []
        self.idea_ids = []

        print("Generating sample data...")
        self.make_users()
        self.make_ideas()
        print("Done.")

    def make_users(self):
        from tools.password import generate_hash
        for i in range(10):
            user_name = "user-{}".format(i + 1)
            user = user_entities.User(
                user_name=user_name,
                password=generate_hash("123123"),
                full_name=self.sd.fullname(locale='us'),
                email=self.sd.word() + '@piweekr.org',
                avatar = {
                    "head": self.sd.int(1, 10),
                    "body": self.sd.int(1, 10),
                    "legs": self.sd.int(1, 10),
                    "background": self.sd.choice(sample_colors),
                }
            )
            user = user_repository.create(user)
            self.user_ids.append(user.id)

    def make_ideas(self):
        for i in range(50):

            emojis = ["thumbsup", "dancer", "confused"]
            reactions_counts = {}
            for j in range(self.sd.int(0, 3)):
                reactions_counts[random.choice(emojis)] = self.sd.int(0, 10)

            idea = idea_entities.Idea(
                uuid=uuid.uuid4().hex,
                title=self.sd.words(5, 10).capitalize(),
                description=self.sd.paragraphs(2, 4),
                owner_id=random.choice(self.user_ids),
                created_at=arrow.get(self.sd.past_datetime()),
                is_public=self.sd.boolean(),
                forked_from=random.choice(self.idea_ids) if self.idea_ids and self.sd.int(1, 8) == 1 else None,
                comments_count=self.sd.int(0, 20),
                reactions_counts= reactions_counts,
            )
            idea = idea_repository.create(idea)
            self.idea_ids.append(idea.id)

