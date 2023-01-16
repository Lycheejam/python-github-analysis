import os
import traceback
import pprint
from dotenv import load_dotenv
from github import Github
from models.pullrequest_model import PullRequest
from models.reviewer_model import Reviewer
from models.setting import session

load_dotenv()


class GithubPullRequestAnalysis:
    def __init__(self) -> None:
        self.g_client = self.authorize_client()

    def main(self):
        repo_list = ["PyGithub/PyGithub"]
        for repo_name in repo_list:
            repo = self.g_client.get_repo(repo_name)
            pullrequests = repo.get_pulls(state="all", sort="created", direction="desc")

            try:
                for pullrequest in pullrequests:
                    merged_at = None
                    if pullrequest.merged_at is not None:
                        merged_at = pullrequest.merged_at

                    merged_by = None
                    if pullrequest.merged_by is not None:
                        merged_by = pullrequest.merged_by.login

                    closed_at = None
                    if pullrequest.closed_at is not None:
                        closed_at = pullrequest.closed_at

                    result = PullRequest(
                        repo=repo_name,
                        p_id=pullrequest.id,
                        p_number=pullrequest.number,
                        base_ref=pullrequest.base.ref,
                        head_ref=pullrequest.head.ref,
                        p_created_at=pullrequest.created_at,
                        p_create_by=pullrequest.user.login,
                        merged_at=merged_at,
                        merged_by=merged_by,
                        closed_at=closed_at,
                    )
                    session.add(result)
                    session.commit()

                    review_events = pullrequest.get_reviews()
                    for review_event in review_events:
                        review = Reviewer(
                            reviewer_id=review_event.id,
                            pullrequest_id=result.id,
                            submitted_at=review_event.submitted_at,
                            submitted_by=review_event.user.login,
                            state=review_event.state,
                        )
                        session.add(review)
                        session.commit()
            except Exception:
                pprint.pprint(traceback.format_exc())
            # TODO: RateLimitExceededExceptionのretry実装

            # file_name = repo_name.split("/")[1] + "_pullrequest.json"
            # file_path = os.path.join(
            #     os.path.dirname(os.path.abspath(__file__)), "../data", file_name
            # )
            # with open(file_path, "w") as f:
            #     json.dump(results, f, indent=4)

    def authorize_client(self):
        return Github(login_or_token=os.environ.get("GITHUB_PAT"))


if __name__ == "__main__":
    github_pullrequest_analysis = GithubPullRequestAnalysis()
    github_pullrequest_analysis.main()
