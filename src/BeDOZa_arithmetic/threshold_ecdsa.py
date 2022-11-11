import random

import ecdsa

from src.own_ecdsa import EllipticCurve


def convert(secret_share):
    EC = EllipticCurve(generator=ecdsa.curves.SECP256k1.generator)
    secret_curve_point = EC.generator * secret_share
    return secret_curve_point


def open_curve_point(secret_share_point_a, secret_share_point_b):
    curve_point = (secret_share_point_a + secret_share_point_b)
    return curve_point

def key_gen():
    EC = EllipticCurve(generator=ecdsa.curves.SECP256k1.generator)

    # Generate a secret key
    sk = random.randint(0, EC.p)

    # Generate secret shares for both alice and bob
    secret_share_alice = random.randint(0, EC.p)
    secret_share_bob = (sk - secret_share_alice) % EC.p
    # Generate public key
    pk = open_curve_point(convert(secret_share_alice), convert(secret_share_bob))

    return secret_share_alice, secret_share_bob, pk


def user_independent_preprocessing():
    pass


def user_dependent_preprocessing():
    pass


def sign_message():
    pass
