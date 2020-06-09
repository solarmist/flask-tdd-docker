import os
import pytest


@pytest.mark.parametrize(
    "environment, expected, invalid",
    [
        pytest.param(
            "project.config.BaseConfig",
            dict(  # Expected values for this environment
                TESTING=False,
                DEBUG=False,
                SQLALCHEMY_TRACK_MODIFICATIONS=False,
                SECRET_KEY="testing_key",
                ENV="development",
            ),
            dict(),  # invalid values for this environment
            id="Base",
        ),
        # Only include the values overridden from Base
        pytest.param(
            "project.config.DevelopmentConfig",
            dict(  # Expected values for this environment
                TESTING=False,
                DEBUG=True,
                JSONIFY_PRETTYPRINT_REGULAR=True,
                PRESERVE_CONTEXT_ON_EXCEPTION=False,
            ),
            dict(),  # invalid values for this environment
            id="Development",
        ),
        pytest.param(
            "project.config.TestingConfig",
            dict(  # Expected values for this environment
                TESTING=True,
                DEBUG=False,
                JSONIFY_PRETTYPRINT_REGULAR=True,
                PRESERVE_CONTEXT_ON_EXCEPTION=True,
            ),
            dict(),  # invalid values for this environment
            id="Testing",
        ),
        pytest.param(
            "project.config.ProductionConfig",
            dict(TESTING=False, DEBUG=False,),  # Expected values for this environment
            dict(  # invalid values for this environment
                # ENV="development",  # We should do sanity checks in staging and production
            ),
            id="Production",
        ),
    ],
)
def test_configs(test_app, environment, expected, invalid):
    # Given
    # The given part describes the state of the world before you begin the behavior you're specifying in
    # this scenario. You can think of it as the pre-conditions to the test.
    # An application instance
    #
    # State of application before the test runs

    # When
    # The when section is that behavior that you're specifying
    #
    # Behavior/logic being tested
    test_app.config.from_object(environment)

    # Then
    # Finally the then section describes the changes you expect due to the specified behavior.
    #
    # the expected changes/results based on the behavior
    for key, value in expected.items():
        assert (
            test_app.config[key] == value
        ), f"{test_app.config[key]} does not match {value} for {key}"

    for key, value in invalid.items():
        assert (
            test_app.config[key] != value
        ), f"{test_app.config[key]} should not match {value} for {key}"
