from pyteal import *
from pyteal.ast.bytes import Bytes
from pyteal_helpers import program
UINT64_MAX = 0xFFFFFFFFFFFFFFFF


def approval():
    # globals
    global_likes = Bytes("likes")  # uint64

    # locals
    local_like = Bytes("local_like")  # uint64
    note = Txn.application_args[1]  # key input uint64

    # no_op
    op_add_note = Bytes("Add")
    op_delete_note = Bytes("Delete")
    op_like = Bytes("Like")
    op_unLike = Bytes("Unlike")

    # scratch variables
    scratch_likes = ScratchVar(TealType.uint64)
    scratch_local_like = ScratchVar(TealType.uint64)

    #
    @Subroutine(TealType.none)
    def like():
        return Seq(
            [
                scratch_likes.store(App.globalGet(global_likes)),
                scratch_local_like.store(App.localGet(Int(0), local_like)),
                # check if account haven't liked yet
                If(
                    scratch_local_like.load() == Int(0)
                )
                .Then(
                    Seq(
                        App.globalPut(global_likes,
                                      scratch_likes.load() + Int(1)),
                        App.localPut(Int(0), local_like,
                                     scratch_local_like.load() + Int(1)),
                    )
                )
                .Else(
                    Reject(),
                ),
                Approve(),
            ]
        )

    @Subroutine(TealType.none)
    def unLike():
        return Seq(
            [
                scratch_likes.store(App.globalGet(global_likes)),
                scratch_local_like.store(App.localGet(Int(0), local_like)),
                # check if account haven't liked yet
                If(
                    scratch_local_like.load() == Int(1)
                )
                .Then(
                    Seq(
                        App.globalPut(global_likes,
                                      scratch_likes.load() - Int(1)),
                        App.localPut(Int(0), local_like,
                                     scratch_local_like.load() - Int(1)),
                    )
                )
                .Else(
                    Reject(),
                ),
                Approve(),
            ]
        )

    @Subroutine(TealType.none)
    def add_note():
        return Seq(
            Assert(
                And(
                    # account has opted-in
                    App.optedIn(Int(0), Int(0)),
                )
            ),
            App.localPut(Txn.sender(), note, Int(1)),
            Approve(),
        )

    @Subroutine(TealType.none)
    def delete_note():
        return Seq(
            Assert(
                And(
                    # check account has opted-in
                    App.optedIn(Int(0), Int(0)),
                    # check note has been added
                    App.localGet(Txn.sender(), note) == Int(1),
                )
            ),
            App.localDel(Txn.sender(), note),
            Approve(),
        )

    return program.event(
        init=Seq(
            [
                App.globalPut(global_likes, Int(0)),
                Approve(),
            ]
        ),
        opt_in=Seq(
            App.localPut(Int(0), local_like, Int(0)),
            Approve(),
        ),
        no_op=Seq(
            Cond(
                [
                    Txn.application_args[0] == op_like,
                    like(),
                ],
                [
                    Txn.application_args[0] == op_unLike,
                    unLike(),
                ],
                [
                    Txn.application_args[0] == op_add_note,
                    add_note(),
                ],
                [
                    Txn.application_args[0] == op_delete_note,
                    delete_note(),
                ],
            ),
            Reject(),
        ),
    )


def clear():
    return Approve()
