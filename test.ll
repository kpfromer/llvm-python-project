; ModuleID = 'tut1_main'
source_filename = "tut1_main"

@.str = private constant [4 x i8] c"%d\0A\00"

define i32 @main() {
entry:
  %mul_add = call i32 (i32, i32, i32, ...) @mul_add(i32 10, i32 2, i32 3)
  %printf = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str, i32 0, i32 0), i32 %mul_add)
  ret i32 0
}

define private i32 @mul_add(i32 %x, i32 %y, i32 %z, ...) {
entry:
  %tmp = mul i32 %x, %y
  %tmp2 = add i32 %tmp, %z
  ret i32 %tmp2
}

declare i32 @printf(i8*, ...)