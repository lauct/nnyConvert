//
//  NNYCAppDelegate.h
//  nnyConvert
//
//  Created by Chun-Ting Liu on 12/8/26.
//  Copyright (c) 2012年 Chun-Ting Liu. All rights reserved.
//

#import <Cocoa/Cocoa.h>

@interface NNYCAppDelegate : NSObject <NSApplicationDelegate>
{
    NSTask *task;
    NSString *utf8lang;
    NSMutableArray *args;
    NSString* srciptPath;
}
@property (assign) IBOutlet NSWindow *window;
- (IBAction)ClearPath:(NSButton *)sender;
- (IBAction)ClickConvert:(NSButton *)sender;
@property (assign) IBOutlet NSTextFieldCell *FilePathTextFieldCell;

@end
