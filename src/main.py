import os
import traceback
import json
import pprint
from dotenv import load_dotenv
from github import Github

load_dotenv()


class GithubPullRequestAnalysis:
    def __init__(self) -> None:
        self.g_client = self.authorize_client()

    def main(self):
        repo_list = ["PyGithub/PyGithub"]
        for repo_name in repo_list:
            repo = self.g_client.get_repo(repo_name)
            pullrequests = repo.get_pulls(state="all", sort="created", direction="desc")

            results = []

            try:
                for pullrequest in pullrequests[:5]:
                    review_events = pullrequest.get_reviews()
                    reviews = []
                    for review_event in review_events:
                        review = {
                            "submitted_by": review_event.user.login,
                            "state": review_event.state,
                            "submitted_at": review_event.submitted_at.strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                        }
                        reviews.append(review)

                    result = {
                        "pullrequest_number": pullrequest.number,
                        "base_ref": pullrequest.base.ref,
                        "head_ref": pullrequest.head.ref,
                        "created_at": pullrequest.created_at.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "create_by": pullrequest.user.login,
                        # fmt: off
                        "merged_at": pullrequest.merged_at.strftime("%Y-%m-%d %H:%M:%S") if pullrequest.merged_at != None else None,  # noqa: E501,E711
                        "merged_by": pullrequest.merged_by.login if pullrequest.merged_by != None else None,  # noqa: E501,E711
                        "closed_at": pullrequest.closed_at.strftime("%Y-%m-%d %H:%M:%S") if pullrequest.closed_at != None else None,  # noqa: E501,E711
                        "reviews": reviews if len(reviews) != 0 else None
                        # noqa: E501,E711
                        # fmt: on
                    }
                    results.append(result)
                    pprint.pprint(self.g_client.get_rate_limit())
            except Exception:
                print(traceback.format_exc())
            # TODO: RateLimitExceededExceptionのretry実装

            file_name = repo_name.split("/")[1] + "_pullrequest.json"
            file_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "../data", file_name
            )
            with open(file_path, "w") as f:
                json.dump(results, f, indent=4)

    def authorize_client(self):
        return Github(login_or_token=os.environ.get("GITHUB_PAT"))


if __name__ == "__main__":
    github_pullrequest_analysis = GithubPullRequestAnalysis()
    github_pullrequest_analysis.main()
