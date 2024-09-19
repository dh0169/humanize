#!/bin/bash

API_URL="http://localhost:5000/api"
COOKIE_JAR_PREFIX="cookies_user_"
TEST_USERS=10
MAX_ROOMS=5

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to make API calls
call_api() {
    local user=$1
    local method=$2
    local endpoint=$3
    local data=$4
    local cookie_jar="${COOKIE_JAR_PREFIX}${user}.txt"

    if [ "$method" = "GET" ]; then
        curl -s -X GET -b $cookie_jar "$API_URL$endpoint"
    else
        curl -s -X $method -b $cookie_jar -c $cookie_jar -H "Content-Type: application/json" -d "$data" "$API_URL$endpoint"
    fi
}

# Function to check API response
check_response() {
    local test_name=$1
    local response=$2
    local expected_message=$3
    local check_success=$4

    echo "Test: $test_name"
    if echo "$response" | jq -e 'has("message")' > /dev/null; then
        local message=$(echo "$response" | jq -r '.message')
        if [[ "$message" == *"$expected_message"* ]]; then
            echo -e "${GREEN}Passed: $expected_message${NC}"
        else
            echo -e "${RED}Failed: Expected '$expected_message', got '$message'${NC}"
        fi
        
        if [ "$check_success" = true ] && echo "$response" | jq -e 'has("did_succeed")' > /dev/null; then
            local success=$(echo "$response" | jq -r '.did_succeed')
            if [ "$success" = true ]; then
                echo -e "${GREEN}Success flag is true${NC}"
            else
                echo -e "${RED}Success flag is false${NC}"
            fi
        fi
    else
        echo -e "${RED}Failed: Response doesn't contain 'message' field${NC}"
        echo "Response: $response"
    fi
    echo ""
}

# Initialize test counter
test_count=0

# Test 1: Check API status
((test_count++))
echo "Test $test_count: Checking API status"
response=$(curl -s -X GET "$API_URL/")
check_response "API Status" "$response" "Chat API is running"

# Register users and perform various actions
for i in $(seq 1 $TEST_USERS); do
    # Test: Register a new user
    ((test_count++))
    echo "Test $test_count: Registering user$i"
    response=$(call_api $i "POST" "/register" "{\"username\": \"user$i\"}")
    check_response "Register user$i" "$response" "Registration Success!" true

    # Test: Get lobby information
    ((test_count++))
    echo "Test $test_count: Getting lobby information for user$i"
    response=$(call_api $i "GET" "/lobby")
    check_response "Lobby info user$i" "$response" "Welcome user$i!"

    # Test: Host a room (for some users)
    if [ $((i % 3)) -eq 0 ]; then
        ((test_count++))
        echo "Test $test_count: User$i hosting a room"
        room_name="room_$((i/3))"
        response=$(call_api $i "POST" "/lobby" "{\"type\": \"host\", \"room\": \"$room_name\"}")
        check_response "Host room $room_name" "$response" "New game session created, $room_name" true
    fi
done

# Join rooms and perform additional tests
for i in $(seq 1 $TEST_USERS); do
    if [ $((i % 3)) -ne 0 ]; then
        # Test: Join a random room
        ((test_count++))
        echo "Test $test_count: User$i joining a random room"
        response=$(call_api $i "POST" "/lobby" '{"type": "join", "random": true}')
        check_response "Join random room user$i" "$response" "has joined" true

        # Test: Try to join another room while active
        ((test_count++))
        echo "Test $test_count: User$i trying to join another room while active"
        response=$(call_api $i "POST" "/lobby" '{"type": "join", "room": "some_room"}')
        check_response "Join room while active user$i" "$response" "is already in a session" false
    fi

    # Test: List lobby sessions
    ((test_count++))
    echo "Test $test_count: Listing lobby sessions for user$i"
    response=$(call_api $i "GET" "/lobby/sessions")
    check_response "List sessions user$i" "$response" "Sessions available to join"

    # Test: List users
    ((test_count++))
    echo "Test $test_count: Listing users for user$i"
    response=$(call_api $i "GET" "/lobby/users")
    check_response "List users user$i" "$response" "Users in game"
done

# Additional edge case tests
# Test: Try to register an existing user
((test_count++))
echo "Test $test_count: Trying to register an existing user"
response=$(call_api 1 "POST" "/register" '{"username": "user1"}')
check_response "Register existing user" "$response" "User already exists" false

# Test: Try to host a room with an empty name
((test_count++))
echo "Test $test_count: Trying to host a room with an empty name"
response=$(call_api 1 "POST" "/lobby" '{"type": "host", "room": ""}')
check_response "Host empty room name" "$response" "room cannot be empty or null" false

# Test: Try to join a non-existent room
((test_count++))
echo "Test $test_count: Trying to join a non-existent room"
response=$(call_api 1 "POST" "/lobby" '{"type": "join", "room": "nonexistent_room"}')
check_response "Join non-existent room" "$response" "Error, nonexistent_room not found!" false

# Logout tests
for i in $(seq 1 $TEST_USERS); do
    # Test: Logout
    ((test_count++))
    echo "Test $test_count: Logging out user$i"
    response=$(call_api $i "GET" "/logout")
    check_response "Logout user$i" "$response" "Logout successful"

    # Test: Try to access protected route after logout
    ((test_count++))
    echo "Test $test_count: Trying to access protected route after logout for user$i"
    response=$(call_api $i "GET" "/lobby")
    check_response "Protected route after logout user$i" "$response" "Please register a username"
done

# Clean up
rm ${COOKIE_JAR_PREFIX}*

echo "All tests completed. Total tests run: $test_count"
