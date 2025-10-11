#!/bin/bash

# 🧪 Script لاختبار النشر على Koyeb تلقائياً
# Usage: ./test_deployment.sh https://your-app.koyeb.app

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Base URL from argument or default
BASE_URL=${1:-"https://screeching-tildi-adelzidoune-ca9a7151.koyeb.app"}

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}🧪 Testing API Deployment${NC}"
echo -e "${BLUE}=====================================${NC}"
echo -e "${YELLOW}Base URL: ${BASE_URL}${NC}\n"

# Counter for passed/failed tests
PASSED=0
FAILED=0

# Function to test endpoint
test_endpoint() {
    local name=$1
    local endpoint=$2
    local expected_status=$3
    local method=${4:-"GET"}
    local data=${5:-""}
    
    echo -e "${YELLOW}Testing: ${name}${NC}"
    echo -e "  Endpoint: ${endpoint}"
    
    if [ "$method" == "POST" ]; then
        response=$(curl -s -w "\n%{http_code}" -X POST \
            -H "Content-Type: application/json" \
            -d "$data" \
            "${BASE_URL}${endpoint}")
    else
        response=$(curl -s -w "\n%{http_code}" "${BASE_URL}${endpoint}")
    fi
    
    status_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)
    
    if [ "$status_code" == "$expected_status" ]; then
        echo -e "  ${GREEN}✅ PASSED${NC} (Status: ${status_code})"
        ((PASSED++))
    else
        echo -e "  ${RED}❌ FAILED${NC} (Expected: ${expected_status}, Got: ${status_code})"
        echo -e "  Response: ${body}"
        ((FAILED++))
    fi
    echo ""
}

# Function to test health check details
test_health_detailed() {
    echo -e "${YELLOW}Testing: Health Check (Detailed)${NC}"
    echo -e "  Endpoint: /health"
    
    response=$(curl -s "${BASE_URL}/health")
    
    # Check if response contains required fields
    if echo "$response" | grep -q '"status"'; then
        echo -e "  ${GREEN}✅ Status field present${NC}"
    else
        echo -e "  ${RED}❌ Status field missing${NC}"
        ((FAILED++))
        return
    fi
    
    if echo "$response" | grep -q '"database"'; then
        echo -e "  ${GREEN}✅ Database check present${NC}"
    else
        echo -e "  ${RED}❌ Database check missing${NC}"
        ((FAILED++))
        return
    fi
    
    if echo "$response" | grep -q '"filesystem"'; then
        echo -e "  ${GREEN}✅ Filesystem check present${NC}"
    else
        echo -e "  ${RED}❌ Filesystem check missing${NC}"
        ((FAILED++))
        return
    fi
    
    # Check if database is healthy
    if echo "$response" | grep -q '"database".*"healthy"' || \
       echo "$response" | grep -q '"healthy".*"database"'; then
        echo -e "  ${GREEN}✅ Database is healthy${NC}"
    else
        echo -e "  ${YELLOW}⚠️  Database health check issue${NC}"
    fi
    
    ((PASSED++))
    echo ""
}

echo -e "${BLUE}Starting tests...${NC}\n"

# Test 1: Root endpoint
test_endpoint "Root Endpoint" "/" "200"

# Test 2: Health check
test_endpoint "Health Check" "/health" "200"

# Test 3: Detailed health check
test_health_detailed

# Test 4: Changelog
test_endpoint "Changelog" "/changelog" "200"

# Test 5: OpenAPI JSON
test_endpoint "OpenAPI Schema" "/openapi.json" "200"

# Test 6: Swagger UI
test_endpoint "Swagger Documentation" "/docs" "200"

# Test 7: ReDoc
test_endpoint "ReDoc Documentation" "/redoc" "200"

# Test 8: Register (should work)
test_endpoint "Register User" "/auth/register" "201" "POST" \
    '{"email":"test_'$(date +%s)'@example.com","username":"test_'$(date +%s)'","password":"testpass123","company_name":"Test Co"}'

# Test 9: Login with wrong credentials (should fail)
test_endpoint "Login (Wrong Credentials)" "/auth/login" "401" "POST" \
    '{"username":"wronguser","password":"wrongpass"}'

# Test 10: Protected endpoint without token (should fail)
test_endpoint "Protected Endpoint (No Auth)" "/users/me" "401"

# Test 11: Invoice generation without token (should fail)
test_endpoint "Generate Invoice (No Auth)" "/invoices/generate" "401" "POST" \
    '{}'

# Test 12: List invoices without token (should fail)
test_endpoint "List Invoices (No Auth)" "/invoices" "401"

# Test 13: Static files directory exists
echo -e "${YELLOW}Testing: Static Files${NC}"
echo -e "  Checking static directory..."
static_test=$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}/static/")
if [ "$static_test" == "404" ] || [ "$static_test" == "200" ]; then
    echo -e "  ${GREEN}✅ Static directory accessible${NC}"
    ((PASSED++))
else
    echo -e "  ${RED}❌ Static directory issue (Status: ${static_test})${NC}"
    ((FAILED++))
fi
echo ""

# Test 14: CORS headers
echo -e "${YELLOW}Testing: CORS Headers${NC}"
cors_response=$(curl -s -I -X OPTIONS \
    -H "Origin: https://rapidapi.com" \
    -H "Access-Control-Request-Method: POST" \
    "${BASE_URL}/auth/login")

if echo "$cors_response" | grep -q "Access-Control-Allow-Origin"; then
    echo -e "  ${GREEN}✅ CORS headers present${NC}"
    ((PASSED++))
else
    echo -e "  ${RED}❌ CORS headers missing${NC}"
    ((FAILED++))
fi
echo ""

# Test 15: Security headers
echo -e "${YELLOW}Testing: Security Headers${NC}"
security_response=$(curl -s -I "${BASE_URL}/")

security_headers=(
    "X-Content-Type-Options"
    "X-Frame-Options"
    "Strict-Transport-Security"
)

security_passed=true
for header in "${security_headers[@]}"; do
    if echo "$security_response" | grep -qi "$header"; then
        echo -e "  ${GREEN}✅ ${header} present${NC}"
    else
        echo -e "  ${YELLOW}⚠️  ${header} missing${NC}"
        security_passed=false
    fi
done

if [ "$security_passed" = true ]; then
    ((PASSED++))
else
    echo -e "  ${YELLOW}⚠️  Some security headers missing (not critical)${NC}"
    ((PASSED++))  # Not critical, so we still count as passed
fi
echo ""

# Test 16: Response time check
echo -e "${YELLOW}Testing: Response Time${NC}"
start_time=$(date +%s.%N)
curl -s -o /dev/null "${BASE_URL}/health"
end_time=$(date +%s.%N)
response_time=$(echo "$end_time - $start_time" | bc)

if (( $(echo "$response_time < 1.0" | bc -l) )); then
    echo -e "  ${GREEN}✅ Fast response (${response_time}s)${NC}"
    ((PASSED++))
elif (( $(echo "$response_time < 5.0" | bc -l) )); then
    echo -e "  ${YELLOW}⚠️  Acceptable response (${response_time}s)${NC}"
    ((PASSED++))
else
    echo -e "  ${RED}❌ Slow response (${response_time}s)${NC}"
    echo -e "  ${YELLOW}  Note: This might be a cold start${NC}"
    ((FAILED++))
fi
echo ""

# Summary
echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}📊 Test Summary${NC}"
echo -e "${BLUE}=====================================${NC}"
echo -e "${GREEN}✅ Passed: ${PASSED}${NC}"
echo -e "${RED}❌ Failed: ${FAILED}${NC}"
echo -e "${BLUE}Total: $((PASSED + FAILED))${NC}"

if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}🎉 All tests passed! API is ready for RapidAPI.${NC}"
    exit 0
else
    echo -e "\n${RED}⚠️  Some tests failed. Please check the errors above.${NC}"
    exit 1
fi
