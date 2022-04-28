; ModuleID = "main"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

declare void @"print"(i32 %".1") 

declare i32 @"input"() 

define i32 @"main"() 
{
entry:
  %"flatten_0" = add i32 0, 22
  %"a" = add i32 0, %"flatten_0"
  %"tmp_0" = add i32 %"a", 55
  %"flatten_1" = add i32 0, %"tmp_0"
  %"flatten_2" = add i32 0, %"flatten_1"
  call void @"print"(i32 %"flatten_2")
  %"tmp_1" = add i32 4, %"a"
  %"flatten_3" = add i32 0, %"tmp_1"
  %"tmp_2" = add i32 %"flatten_3", %"a"
  %"flatten_4" = add i32 0, %"tmp_2"
  %"flatten_5" = add i32 0, %"flatten_4"
  %"a.1" = add i32 0, %"flatten_5"
  %"flatten_6" = add i32 0, %"a.1"
  call void @"print"(i32 %"flatten_6")
  ret i32 0
}
