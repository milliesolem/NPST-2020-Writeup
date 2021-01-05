
const { assemble, step } = require("@pstnorge/slede8");
const tellPingviner = (flag, input) => {
    const sourceCode = tellPingvinerImpl(flag);
    
    const { exe } = assemble(sourceCode);
    const iter = step(exe, input, 2500);
    while (iter) {
        try {
            const tick = iter.next()
            if (tick.done) {
                return [...Buffer.from(tick.value.stdout)];
            }
        }
        catch (e) {
            throw e;
        }
     }
}

const tellPingvinerImpl = (flag) => `
SETT r10, 0
SETT r11, 1
HOPP forbi

flagg:
.DATA ${Buffer.from(flag).join(",")},0

print:
LAST r2
PLUSS r0, r11
LIK r2, r10
BHOPP print_ferdig
SKRIV r2
HOPP print
print_ferdig:
RETUR

input_buffer:
.DATA 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
.DATA 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
.DATA 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
.DATA 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
.DATA 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
.DATA 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
.DATA 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
.DATA 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

forbi:
TUR les_input
TUR tell_pingviner
TUR skriv_svar
fin:
STOPP


les_input:
FINN input_buffer
les_neste_input:
LES r2
; ULK r2, r11 ; dette funker ikke...
LIK r2, r10
BHOPP lest_ferdig
LAGR r2
PLUSS r0, r11
HOPP les_neste_input

lest_ferdig:
RETUR

tell_pingviner:
SETT r4, 0
FINN input_buffer

lik_0xf0:
TUR last_neste
LIK r2, r10
BHOPP telt_pingviner

SETT r3, 0xf0
LIK r2, r3
BHOPP lik_0x9f
HOPP lik_0xf0

lik_0x9f:
TUR last_neste
SETT r3, 0x9f
LIK r2, r3
BHOPP lik_0x90
HOPP lik_0xf0

lik_0x90:
TUR last_neste
SETT r3, 0x90
LIK r2, r3
BHOPP lik_0xa7
HOPP lik_0xf0

lik_0xa7:
TUR last_neste
SETT r3, 0xa7
LIK r2, r3
BHOPP pingvin_funnet
HOPP lik_0xf0

pingvin_funnet:
PLUSS r4, r11
HOPP lik_0xf0 


telt_pingviner:
SETT r2, r4
RETUR

last_neste:
LAST r2
PLUSS r0, r11
RETUR

skriv_svar:
SKRIV r2
RETUR
`


module.exports = {
    tellPingviner
}
