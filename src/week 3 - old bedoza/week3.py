from dealer import Dealer
from alice import Alice
from bob import Bob
from util import create_bit_array_from_bit_string, btformula_from_class


def test_bedoza(x_as_bit_string, y_as_bit_string):
    x_as_bit_array = create_bit_array_from_bit_string(x_as_bit_string)
    y_as_bit_array = create_bit_array_from_bit_string(y_as_bit_string)

    # Initialization
    dealer = Dealer()
    rand_a = dealer.rand_a()
    rand_b = dealer.rand_b()
    alice = Alice(x_as_bit_array, rand_a)
    bob = Bob(y_as_bit_array, rand_b)
    alice.receive_input_share_from_other_participant(bob.send_input_share_to_alice())
    bob.receive_input_share_from_other_participant(alice.send_input_share_to_bob())

    # Compute layer 1 - Only Alice does work in layer 1.
    alice.compute_layer1()

    # Compute layer 2 - This requires an intermediate step where the parties open e and d shares
    alice.compute_layer2_before_open()
    bob.compute_layer2_before_open()
    alice.receive_d_shares_from_other_participant(bob.open_d_shares_to_alice())
    bob.receive_d_shares_from_other_participant(alice.open_d_shares_to_bob())
    alice.receive_e_shares_from_other_participant(bob.open_e_shares_to_alice())
    bob.receive_e_shares_from_other_participant(alice.open_e_shares_to_bob())
    alice.compute_rest_of_layer2()
    bob.compute_rest_of_layer2()

    # Compute layer 3 - Only Alice does work in layer 3.
    alice.compute_layer3()

    # Compute layer 4 - This requires an intermediate step where the parties open e and d shares
    alice.compute_layer4_before_open()
    bob.compute_layer4_before_open()
    alice.receive_d_shares_from_other_participant(bob.open_d_shares_to_alice())
    bob.receive_d_shares_from_other_participant(alice.open_d_shares_to_bob())
    alice.receive_e_shares_from_other_participant(bob.open_e_shares_to_alice())
    bob.receive_e_shares_from_other_participant(alice.open_e_shares_to_bob())
    alice.compute_rest_of_layer4()
    bob.compute_rest_of_layer4()

    # Compute layer 5 - This requires an intermediate step where the parties open e and d shares
    alice.compute_layer5_before_open()
    bob.compute_layer5_before_open()
    alice.receive_d_shares_from_other_participant(bob.open_d_shares_to_alice())
    bob.receive_d_shares_from_other_participant(alice.open_d_shares_to_bob())
    alice.receive_e_shares_from_other_participant(bob.open_e_shares_to_alice())
    bob.receive_e_shares_from_other_participant(alice.open_e_shares_to_bob())
    alice.compute_rest_of_layer5()
    bob.compute_rest_of_layer5()

    return alice.output(bob)


def test_bedoza_on_every_possible_input():
    # All possibilities for recipient blood type "000".
    result = test_bedoza("000", "000")
    assert result == btformula_from_class("000", "000")

    result = test_bedoza("000", "001")
    assert result == btformula_from_class("000", "001")

    result = test_bedoza("000", "010")
    assert result == btformula_from_class("000", "010")

    result = test_bedoza("000", "011")
    assert result == btformula_from_class("000", "011")

    result = test_bedoza("000", "100")
    assert result == btformula_from_class("000", "100")

    result = test_bedoza("000", "101")
    assert result == btformula_from_class("000", "101")

    result = test_bedoza("000", "110")
    assert result == btformula_from_class("000", "110")

    result = test_bedoza("000", "111")
    assert result == btformula_from_class("000", "111")

    # All possibilities for recipient blood type "001".
    result = test_bedoza("001", "000")
    assert result == btformula_from_class("001", "000")

    result = test_bedoza("001", "001")
    assert result == btformula_from_class("001", "001")

    result = test_bedoza("001", "010")
    assert result == btformula_from_class("001", "010")

    result = test_bedoza("001", "011")
    assert result == btformula_from_class("001", "011")

    result = test_bedoza("001", "100")
    assert result == btformula_from_class("001", "100")

    result = test_bedoza("001", "101")
    assert result == btformula_from_class("001", "101")

    result = test_bedoza("001", "110")
    assert result == btformula_from_class("001", "110")

    result = test_bedoza("001", "111")
    assert result == btformula_from_class("001", "111")

    # All possibilities for recipient blood type "010".
    result = test_bedoza("010", "000")
    assert result == btformula_from_class("010", "000")

    result = test_bedoza("010", "001")
    assert result == btformula_from_class("010", "001")

    result = test_bedoza("010", "010")
    assert result == btformula_from_class("010", "010")

    result = test_bedoza("010", "011")
    assert result == btformula_from_class("010", "011")

    result = test_bedoza("010", "100")
    assert result == btformula_from_class("010", "100")

    result = test_bedoza("010", "101")
    assert result == btformula_from_class("010", "101")

    result = test_bedoza("010", "110")
    assert result == btformula_from_class("010", "110")

    result = test_bedoza("010", "111")
    assert result == btformula_from_class("010", "111")

    # All possibilities for recipient blood type "011".
    result = test_bedoza("011", "000")
    assert result == btformula_from_class("011", "000")

    result = test_bedoza("011", "001")
    assert result == btformula_from_class("011", "001")

    result = test_bedoza("011", "010")
    assert result == btformula_from_class("011", "010")

    result = test_bedoza("011", "011")
    assert result == btformula_from_class("011", "011")

    result = test_bedoza("011", "100")
    assert result == btformula_from_class("011", "100")

    result = test_bedoza("011", "101")
    assert result == btformula_from_class("011", "101")

    result = test_bedoza("011", "110")
    assert result == btformula_from_class("011", "110")

    result = test_bedoza("011", "111")
    assert result == btformula_from_class("011", "111")

    # All possibilities for recipient blood type "100".
    result = test_bedoza("100", "000")
    assert result == btformula_from_class("100", "000")

    result = test_bedoza("100", "001")
    assert result == btformula_from_class("100", "001")

    result = test_bedoza("100", "010")
    assert result == btformula_from_class("100", "010")

    result = test_bedoza("100", "011")
    assert result == btformula_from_class("100", "011")

    result = test_bedoza("100", "100")
    assert result == btformula_from_class("100", "100")

    result = test_bedoza("100", "101")
    assert result == btformula_from_class("100", "101")

    result = test_bedoza("100", "110")
    assert result == btformula_from_class("100", "110")

    result = test_bedoza("100", "111")
    assert result == btformula_from_class("100", "111")

    # All possibilities for recipient blood type "101".
    result = test_bedoza("101", "000")
    assert result == btformula_from_class("101", "000")

    result = test_bedoza("101", "001")
    assert result == btformula_from_class("101", "001")

    result = test_bedoza("101", "010")
    assert result == btformula_from_class("101", "010")

    result = test_bedoza("101", "011")
    assert result == btformula_from_class("101", "011")

    result = test_bedoza("101", "100")
    assert result == btformula_from_class("101", "100")

    result = test_bedoza("101", "101")
    assert result == btformula_from_class("101", "101")

    result = test_bedoza("101", "110")
    assert result == btformula_from_class("101", "110")

    result = test_bedoza("101", "111")
    assert result == btformula_from_class("101", "111")

    # All possibilities for recipient blood type "110".
    result = test_bedoza("110", "000")
    assert result == btformula_from_class("110", "000")

    result = test_bedoza("110", "001")
    assert result == btformula_from_class("110", "001")

    result = test_bedoza("110", "010")
    assert result == btformula_from_class("110", "010")

    result = test_bedoza("110", "011")
    assert result == btformula_from_class("110", "011")

    result = test_bedoza("110", "100")
    assert result == btformula_from_class("110", "100")

    result = test_bedoza("110", "101")
    assert result == btformula_from_class("110", "101")

    result = test_bedoza("110", "110")
    assert result == btformula_from_class("110", "110")

    result = test_bedoza("110", "111")
    assert result == btformula_from_class("110", "111")

    # All possibilities for recipient blood type "111".
    result = test_bedoza("111", "000")
    assert result == btformula_from_class("111", "000")

    result = test_bedoza("111", "001")
    assert result == btformula_from_class("111", "001")

    result = test_bedoza("111", "010")
    assert result == btformula_from_class("111", "010")

    result = test_bedoza("111", "011")
    assert result == btformula_from_class("111", "011")

    result = test_bedoza("111", "100")
    assert result == btformula_from_class("111", "100")

    result = test_bedoza("111", "101")
    assert result == btformula_from_class("111", "101")

    result = test_bedoza("111", "110")
    assert result == btformula_from_class("111", "110")

    result = test_bedoza("111", "111")
    assert result == btformula_from_class("111", "111")

    print("All 64 tests of the BeDOZa protocol passed successfully.")


test_bedoza_on_every_possible_input()
