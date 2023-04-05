#include "lab-pass.h"
#include "llvm/Analysis/CallGraph.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/Constants.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/Type.h"
#include "llvm/Transforms/Utils/Cloning.h"

using namespace llvm;

char LabPass::ID = 0;

bool LabPass::doInitialization(Module &M) {
    return true;
}

static FunctionCallee printfPrototype(Module &M) {  // example code
    LLVMContext &ctx = M.getContext();
    FunctionType *printfType = FunctionType::get(
        Type::getInt32Ty(ctx),
        {Type::getInt8PtrTy(ctx)},
        true);
    FunctionCallee printfCallee = M.getOrInsertFunction("printf", printfType);
    return printfCallee;
}

bool LabPass::runOnModule(Module &M) {
    errs() << "runOnModule\n";

    for (auto &F : M) {
        StringRef funcName = F.getName();
        errs() << funcName << "\n";

        LLVMContext &context = M.getContext();
        IRBuilder<> builder(context);

        if (!F.isDeclaration()) {
            builder.SetInsertPoint(&F.getEntryBlock().front());
            Value *funcPtr = builder.CreatePointerCast(
                ConstantExpr::getBitCast(&F, Type::getInt32Ty(context)),
                Type::getInt8PtrTy(context));
            FunctionCallee printfCallee = printfPrototype(M);
            builder.CreateCall(printfCallee, {builder.CreateGlobalStringPtr(funcName.str() + ": %p\n"), funcPtr});
        }
    }
    return true;
}

static RegisterPass<LabPass> X("labpass", "Lab Pass", false, false);
