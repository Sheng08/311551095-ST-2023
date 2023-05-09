/*
  Ref:
  * https://llvm.org/doxygen/
  * https://llvm.org/docs/GettingStarted.html
  * https://llvm.org/docs/WritingAnLLVMPass.html
  * https://llvm.org/docs/ProgrammersManual.html
 */
#include "lab-pass.h"

#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/Constants.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/Type.h"
#include "llvm/IR/Value.h"

using namespace llvm;

char LabPass::ID = 0;

bool LabPass::doInitialization(Module &M) {
    return true;
}

static FunctionCallee printfPrototype(Module &M) {
    LLVMContext &ctx = M.getContext();
    FunctionType *printfType = FunctionType::get(Type::getInt32Ty(ctx),
                                                 {Type::getInt8PtrTy(ctx)}, true);
    FunctionCallee printfCallee = M.getOrInsertFunction("printf", printfType);

    return printfCallee;
}

bool LabPass::runOnModule(Module &M) {
    errs() << "runOnModule\n";

    LLVMContext &ctx = M.getContext();

    // Get the reference of "printf" function prototype in module
    FunctionCallee printfCallee = printfPrototype(M);

    // Create GlobalVariable to save depth of the function (call stack)
    GlobalVariable *depth_GV = new GlobalVariable(M, Type::getInt32Ty(ctx), false,
                                                  GlobalValue::ExternalLinkage, ConstantInt::get(Type::getInt32Ty(ctx), 0), "depth");
    for (auto &F : M) {
        // skip external function. e.g. printf
        if (F.isDeclaration()) continue;

        errs() << F.getName() << "\n";

        // Insert increase depth instruction -> when entry function then increase call stack depth
        // ref. https://stackoverflow.com/questions/30228575/how-to-increment-a-global-variable-in-a-llvm-module
        IRBuilder<> IRB_Entry(&F.getEntryBlock(), F.getEntryBlock().begin());
        LoadInst *load_in = IRB_Entry.CreateLoad(Type::getInt32Ty(ctx), depth_GV, "depth_in");
        Value *inc_in = IRB_Entry.CreateAdd(load_in, IRB_Entry.getInt32(1));
        IRB_Entry.CreateStore(inc_in, depth_GV);

        // Insert printf -> print call stack depth, function name, function address
        Constant *formatStr = IRB_Entry.CreateGlobalStringPtr("%*s" + F.getName().str() + ": %p\n");
        Constant *indent = IRB_Entry.CreateGlobalStringPtr("");
        IRB_Entry.CreateCall(printfCallee, {formatStr, load_in, indent, &F});

        // Insert decrease depth instruction -> when exit function then decrease call stack depth
        IRBuilder<> IRB_Exit(&*(F.back().rbegin()));
        LoadInst *load_out = IRB_Exit.CreateLoad(Type::getInt32Ty(ctx), depth_GV, "depth_out");
        Value *inc_out = IRB_Exit.CreateSub(load_out, IRB_Exit.getInt32(1));
        IRB_Exit.CreateStore(inc_out, depth_GV);
    }
    return true;
}
static RegisterPass<LabPass> X("labpass", "Lab Pass", false, false);