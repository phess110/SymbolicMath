import Token
import Tokenizer

Token.Variable("x")
Token.Variable("y")
Token.Variable("z")
Token.Variable("w")

def test(str):
    Tokenizer.Initialize(str)
    print(str)
    Tokenizer.Tokenize()

test("1+1")
test("1e10-1")
test("1e10 -  1 ")
test("1e-10 * 1")
test("1e-10. ^ 1")
test("( 1e-10 ) / .1")
test("( 1e-10 ) / .1e.1")
test("( 1e-10 ) / .1")

test("0.123 / -0.")
test("   121e0.123   /  -0.e9             ")
test("x * y * z * w")
test("x*y*z*w")
test("xy")

test("sin cos sin cos tan x")
test("exp(ln(log ( lg( cot (x) )) ) )")
test("x ^ y + -z")
test("exp  x +  1e-0.1 * y sin(z^2.0)")
test("exp (x + 2 * 8 * y)")
test("exp (u)")
test("ExP (x)")
test("lOG (x)")
test(" SIN (x)  ")
test("pow(1,2)")
test("1 + 2.0 + .3x + -4.1*y ")
