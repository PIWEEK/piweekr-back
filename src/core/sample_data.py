from sampledata.helper import SampleData

from .users import user_entities
from services.repository.sql.users import user_repository


class SampleData():
    sd = SampleData(seed=1234567890)

    def run(self):
        # Skip sample data if there are already some data
        user_1 = user_repository.retrieve_by_user_name('user-1')
        if user_1:
            return

        print("Generating sample data...")
        self.make_users()
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
                avatar=None,
            )
            user_repository.create(user)

