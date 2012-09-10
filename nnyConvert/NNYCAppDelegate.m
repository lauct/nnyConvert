//
//  NNYCAppDelegate.m
//  nnyConvert
//
//  Created by Chun-Ting Liu on 12/8/26.
//  Copyright (c) 2012年 Chun-Ting Liu. All rights reserved.
//

#import "NNYCAppDelegate.h"

@implementation NNYCAppDelegate
@synthesize FilePathTextFieldCell;

- (void)dealloc
{
    [super dealloc];
}

- (void)applicationDidFinishLaunching:(NSNotification *)aNotification
{
    // Insert code here to initialize your application
    //    char* lang = getenv("LANG");
    task = [[NSTask alloc] init];
    utf8lang = [[NSString alloc] init];
	utf8lang = @"zh_TW.UTF-8";
    args = [[NSMutableArray alloc] init];
    
    srciptPath = [[NSString alloc] initWithString:[[NSBundle mainBundle] pathForResource:@"g2butf8" ofType:@"py"]];
    NSLog(@"srciptPath: %@", srciptPath);
    
}



-(void)processConvert:(NSString*)filePath {
    
    [task setLaunchPath:@"/usr/bin/python"];
    [args addObject:srciptPath];
//    [args addObject:@"/Users/chun/Downloads/g2butf8/g2butf8.py"];
    if (filePath!=nil)
    {
        [args addObject:(NSString*)filePath];
        [task setArguments:args];
        [task setEnvironment:[NSDictionary dictionaryWithObject:utf8lang forKey:@"LC_ALL"]];
        
        [task launch];
    } else
    {
        exit(0);
    }
    
    
    
}
- (IBAction)ClearPath:(id)sender {
    FilePathTextFieldCell.title = @"";
    NSLog(@"clear path");
}

- (IBAction)ClickConvert:(NSButton *)sender {
    NSLog(@"click convert");

    [self processConvert:FilePathTextFieldCell.title];
//    [self processConvert:@"/Users/chun/Downloads/g2butf8/SFII.cn.srt"];

}


@end
