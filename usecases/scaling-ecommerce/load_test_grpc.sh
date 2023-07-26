#/bin/sh

HOST=localhost:50051
TOTAL=100000
CONCURRENCY=50
echo "Querying count of customers:  $TOTAL requests and $CONCURRENCY concurrency"
ghz --insecure --proto .dozer/api/customers/v0001/common.proto --call dozer.common.CommonGrpcService.query --total $TOTAL --concurrency $CONCURRENCY --data '{"endpoint":"customers"}' $HOST