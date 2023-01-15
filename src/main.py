import os
import pprint
from dotenv import load_dotenv
from github import Github

load_dotenv()


class GithubPullRequestAnalysis:
    def __init__(self) -> None:
        self.g_client = self.authorize_client()

    def main(self):
        repo = self.g_client.get_repo("PyGithub/PyGithub")
        pullrequests = repo.get_pulls(state="all", sort="created", direction="desc")
        for pullrequest in pullrequests:
            pprint.pprint(pullrequest.number)
            pprint.pprint(pullrequest.user.email)
            pprint.pprint(pullrequest.base.ref)
            pprint.pprint(pullrequest.head.ref)
            pprint.pprint(pullrequest.created_at)
            pprint.pprint(pullrequest.merged_at)
            pprint.pprint(pullrequest.merged_by.email)
            pprint.pprint(pullrequest.closed_at)

    def authorize_client(self):
        return Github(login_or_token=os.environ.get("GITHUB_PAT"))


if __name__ == "__main__":
    github_pullrequest_analysis = GithubPullRequestAnalysis()
    github_pullrequest_analysis.main()
