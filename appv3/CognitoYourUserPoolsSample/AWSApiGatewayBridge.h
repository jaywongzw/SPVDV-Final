#import <AWSAPIGateway/AWSAPIGateway.h>
	
@interface AWSAPIGatewayClient ()
	
// Networking	
@property (nonatomic, strong) NSURLSession *session;
	
// For requests
@property (nonatomic, strong) NSURL *baseURL;
	
// For responses
@property (nonatomic, strong) NSDictionary *HTTPHeaderFields;
@property (nonatomic, assign) NSInteger HTTPStatusCode;

- (AWSTask *)invokeHTTPRequest:(NSString *)HTTPMethod	
                     URLString:(NSString *)URLString	
                pathParameters:(NSDictionary *)pathParameters	
               queryParameters:(NSDictionary *)queryParameters	
              headerParameters:(NSDictionary *)headerParameters	
                          body:(id)body	
                 responseClass:(Class)responseClass;

@end

@interface AWSServiceConfiguration()

@property (nonatomic, strong) AWSEndpoint *endpoint;

@end
