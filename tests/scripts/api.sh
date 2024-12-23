#!/usr/bin/env bash

# Base URL for the API
BASE_URL="http://127.0.0.1:5000/v1/api/users"

# Usage function
function usage() {
    echo
    echo "Usage: $0 [--tests <test1,test2,...|test1 test2 ...>]"
    echo
    echo "    Example: $0 --tests test_register_user,test_login_user"
    echo
    echo "Description: "
    echo "    Runs the specified tests. If no tests are provided, all tests will run."
}

# Helper function to print test result
function print_result() {
    local actual_status="$1"
    local expected_status="$2"
    local test_name="$3"
    local response_body="$4"

    if [[ "$actual_status" == "$expected_status" ]]; then
        echo "✅ $test_name: Passed"
    else
        echo "❌ $test_name: Failed"
        echo
        echo "Expected HTTP Status: $expected_status, Got: $actual_status"
        echo
        echo "Response Body:"
        echo "$response_body" | jq .
    fi
}

# Utility function to perform a request and capture both status code and body
function api_request() {
    local method="$1"
    local endpoint="$2"
    local data="$3"

    # Perform the request and capture status code and body
    local response
    response=$(curl -s -w "HTTP_CODE:%{http_code}" -X "$method" "$BASE_URL/$endpoint" \
        -H "Content-Type: application/json" \
        -d "$data")

    # Extract the HTTP status code
    local http_code
    http_code=$(echo "$response" | sed -n 's/.*HTTP_CODE:\([0-9]*\)$/\1/p')

    # Extract the response body
    local body
    body=$(echo "$response" |  sed -n '/{/,/}/p')

    # Return the status code and body as a space-separated string
    echo "$http_code $body"
}

# Test: Register a new user
function test_register_user() {
    local response
    response=$(api_request "POST" "register" '{"email": "test@example.com", "password": "password123"}')
    local http_code body
    http_code=$(echo "$response" | awk '{print $1}')
    body=$(echo "$response" | cut -d' ' -f2-)

    print_result "$http_code" 201 " Register User" "$body"
}

# Test: Register a duplicate user
function test_register_duplicate_user() {
    local response
    response=$(api_request "POST" "register" '{"email": "test@example.com", "password": "password123"}')
    local http_code body
    http_code=$(echo "$response" | awk '{print $1}')
    body=$(echo "$response" | cut -d' ' -f2-)

    print_result "$http_code" 400 " Register Duplicate User" "$body"
}

# Test: Login with valid credentials
function test_login_user() {
    local response
    response=$(api_request "POST" "login" '{"email": "test@example.com", "password": "password123"}')
    local http_code body
    http_code=$(echo "$response" | awk '{print $1}')
    body=$(echo "$response" | cut -d' ' -f2-)

    if [ "$http_code" -eq 200 ] && [[ "$body" == *"token"* ]]; then
        echo "✅ Login User: Passed"
    else
        echo "❌ Login User: Failed"
        echo "   HTTP Code: $http_code"
        echo "   Response Body: $body"
    fi
}

# Test: Login with invalid credentials
function test_login_invalid_user() {
    local response
    response=$(api_request "POST" "login" '{"email": "invalid@example.com", "password": "wrongpassword"}')
    local http_code body
    http_code=$(echo "$response" | awk '{print $1}')
    body=$(echo "$response" | cut -d' ' -f2-)

    print_result "$http_code" 401 " Login Invalid User" "$body"
}

# Test: Get user profile
function test_get_user_profile() {
    # Login to get the token
    local login_response
    login_response=$(api_request "POST" "login" '{"email": "test@example.com", "password": "password123"}')
    local token_http_code token_body
    token_http_code=$(echo "$login_response" | awk '{print $1}')
    token_body=$(echo "$login_response" | cut -d' ' -f2-)

    local token
    token=$(echo "$token_body" | jq -r '.token')

    # If login fails, report and return
    if [ "$token_http_code" -ne 200 ] || [ "$token" == "null" ]; then
        echo "❌ Get User Profile: Failed to login for token"
        echo "   HTTP Code: $token_http_code"
        echo "   Response Body: $token_body"
        return
    fi

    # Make profile request with the token
    local profile_response
    profile_response=$(curl -s -w "HTTP_CODE:%{http_code}" -X GET "$BASE_URL/profile" \
        -H "x-access-token: $token")
    local profile_http_code profile_body
    profile_http_code=$(echo "$profile_response" | awk '{print $1}')
    profile_body=$(echo "$profile_response" | cut -d' ' -f2-)

    print_result "$profile_http_code" 200 " Get User Profile" "$profile_body"
}

# Run selected tests
function run_tests() {
    TESTS_TO_RUN=("$@")

    for TEST in "${TESTS_TO_RUN[@]}"; do
        if declare -f "$TEST" > /dev/null; then
            $TEST
        else
            echo "❌ Unknown test: $TEST"
        fi
    done
}

# Default: Run all tests if no arguments provided
ALL_TESTS=( \
  test_register_user \
  test_register_duplicate_user \
  test_login_user \
  test_login_invalid_user \
  test_get_user_profile \
)

# Parse arguments
if [ "$#" -eq 0 ]; then
    run_tests "${ALL_TESTS[@]}"
else
    case "$1" in
        --tests)
            if [ -z "$2" ]; then
                usage
                exit 1
            fi
            # Split the tests argument into an array (comma or space separated)
            IFS=', ' read -r -a SELECTED_TESTS <<< "$2"
            run_tests "${SELECTED_TESTS[@]}"
            ;;
        *)
            usage
            exit 1
            ;;
    esac
fi
