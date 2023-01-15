import os
import traceback
import json
from dotenv import load_dotenv
from github import Github

load_dotenv()


class GithubPullRequestAnalysis:
    def __init__(self) -> None:
        self.g_client = self.authorize_client()

    def main(self):
        repo = self.g_client.get_repo("PyGithub/PyGithub")
        pullrequests = repo.get_pulls(state="all", sort="created", direction="desc")

        results = []

        try:
            for pullrequest in pullrequests[:5]:
                result = {
                    "pullrequest_number": pullrequest.number,
                    "base_ref": pullrequest.base.ref,
                    "head_ref": pullrequest.head.ref,
                    "created_at": pullrequest.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "create_by": pullrequest.user.email,
                    # fmt: off
                    "merged_at": pullrequest.merged_at.strftime("%Y-%m-%d %H:%M:%S") if pullrequest.merged_at != None else None,  # noqa: E501,E711
                    "merged_by": pullrequest.merged_by.email if pullrequest.merged_by != None else None,  # noqa: E501,E711
                    "closed_at": pullrequest.closed_at.strftime("%Y-%m-%d %H:%M:%S") if pullrequest.closed_at != None else None  # noqa: E501,E711
                    # fmt: on
                }
                results.append(result)
        except Exception:
            print(traceback.format_exc())

        with open("pullrequests.json", "w") as f:
            json.dump(results, f, indent=4)

    def authorize_client(self):
        return Github(login_or_token=os.environ.get("GITHUB_PAT"))


if __name__ == "__main__":
    github_pullrequest_analysis = GithubPullRequestAnalysis()
    github_pullrequest_analysis.main()
