#!/bin/bash

API_URL="https://humanize.live/api"
COOKIE_JAR_PREFIX="cookies_user_"
TEST_USERS=3

# Color output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Initialize result storage
JSON_RESULTS=()
declare -A TEST_METADATA
test_count=0

# API call wrapper
call_api() {
    local user=$1 method=$2 endpoint=$3 data=$4
    local cookie_jar="${COOKIE_JAR_PREFIX}${user}.txt"
    if [ "$method" = "GET" ]; then
        curl -s -X GET -b $cookie_jar "$API_URL$endpoint"
    else
        curl -s -X $method -b $cookie_jar -c $cookie_jar -H "Content-Type: application/json" -d "$data" "$API_URL$endpoint"
    fi
}

# Record result
record_test() {
    local id=$1 name=$2 status=$3 expected=$4 actual=$5 success=$6
    local type=${TEST_METADATA["$id,type"]}
    local desc=${TEST_METADATA["$id,desc"]}

    JSON_RESULTS+=("$(jq -n \
        --arg id "$id" \
        --arg name "$name" \
        --arg type "$type" \
        --arg desc "$desc" \
        --arg status "$status" \
        --arg expected "$expected" \
        --arg actual "$actual" \
        --argjson success "${success:-null}" \
        '{id: $id|tonumber, name: $name, description: $desc, type: $type, status: $status, expected_message: $expected, actual_message: $actual, did_succeed: $success}')")
}

# Evaluate response
check_response() {
    local test_name=$1 response=$2 expected=$3 success_check=$4
    local status="failed" actual="" success="null"

    echo "Test: $test_name"

    if echo "$response" | jq -e 'has("message")' > /dev/null; then
        actual=$(echo "$response" | jq -r '.message')
        if [[ "$actual" == *"$expected"* ]]; then
            status="passed"
            echo -e "${GREEN}Passed: $expected${NC}"
        else
            echo -e "${RED}Failed: Expected '$expected', got '$actual'${NC}"
        fi
        if [ "$success_check" = true ]; then
            success=$(echo "$response" | jq -r '.did_succeed')
        fi
    else
        actual="Invalid response structure"
        echo -e "${RED}Invalid response${NC}"
    fi
    echo ""
    record_test "$test_count" "$test_name" "$status" "$expected" "$actual" "$success"
}

# ----------- TESTS -----------

# Test 1: API Status
((test_count++))
TEST_METADATA["$test_count,type"]="integration"
TEST_METADATA["$test_count,desc"]="Checks if the API is online and returns a status message."
response=$(curl -s "$API_URL/")
check_response "API Status Check" "$response" "Chat API is running"

# Test 2: Register user1
((test_count++))
TEST_METADATA["$test_count,type"]="unit"
TEST_METADATA["$test_count,desc"]="Register a new user and check for success message."
response=$(call_api 1 "POST" "/register" '{"username": "user1"}')
check_response "Register User" "$response" "Registration Success!" true

# Test 3: Get lobby info
((test_count++))
TEST_METADATA["$test_count,type"]="integration"
TEST_METADATA["$test_count,desc"]="User retrieves welcome message from lobby."
response=$(call_api 1 "GET" "/lobby")
check_response "Lobby Info" "$response" "Welcome user1!"

# Test 4: Host room
((test_count++))
TEST_METADATA["$test_count,type"]="integration"
TEST_METADATA["$test_count,desc"]="User hosts a game room and expects success confirmation."
response=$(call_api 1 "POST" "/lobby" '{"type": "host", "room": "alpha"}')
check_response "Host Room" "$response" "New game session created" true

# Test 5: Join nonexistent room
((test_count++))
TEST_METADATA["$test_count,type"]="edge"
TEST_METADATA["$test_count,desc"]="Try joining a room that doesn't exist."
response=$(call_api 1 "POST" "/lobby" '{"type": "join", "room": "ghostroom"}')
check_response "Join Invalid Room" "$response" "not found" false

# ---------- OUTPUTS -----------

# JSON output
echo "[" > test_results.json
for i in "${!JSON_RESULTS[@]}"; do
    echo "${JSON_RESULTS[$i]}" >> test_results.json
    [ "$i" -lt $(( ${#JSON_RESULTS[@]} - 1 )) ] && echo "," >> test_results.json
done
echo "]" >> test_results.json

# Markdown summary
echo "| ID | Name | Type | Status |" > test_results.md
echo "|----|------|------|--------|" >> test_results.md
for result in "${JSON_RESULTS[@]}"; do
    id=$(echo "$result" | jq '.id')
    name=$(echo "$result" | jq -r '.name')
    type=$(echo "$result" | jq -r '.type')
    status=$(echo "$result" | jq -r '.status')
    echo "| $id | $name | $type | $status |" >> test_results.md
done

# Cleanup
rm ${COOKIE_JAR_PREFIX}* 2>/dev/null

echo "Tests complete. Results saved to test_results.json and test_results.md"
