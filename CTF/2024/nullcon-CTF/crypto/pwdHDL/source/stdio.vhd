library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.textio.all;

package stdio is
	procedure write_stdout(str: in STRING);	
	impure function read_stdin(n: in POSITIVE) return STRING;
	impure function read_urandom(n: in POSITIVE) return STD_LOGIC_VECTOR;
end package;

package body stdio is
	procedure write_stdout(str: in STRING) is
		variable buf : LINE;
	begin
		write(buf, str);
		writeline(output, buf);
	end procedure;
	
	impure function read_stdin(n: in POSITIVE) return STRING is
		variable inbuf : LINE;
		variable outbuf : STRING(1 to n) := (others => '0');
	begin
		write(output, "> ");
		if not endfile(input) then
			readline(input, inbuf);
			if inbuf'length > 0 then
				read(inbuf, outbuf(1 to minimum(inbuf'length, n)));
			end if;
		else
			write_stdout("Failed to read from stdin.");
			std.env.stop;
		end if;
		return outbuf;
	end function;

	impure function read_urandom(n: in POSITIVE) return STD_LOGIC_VECTOR is
		TYPE T_CHARFILE IS FILE OF CHARACTER;
		FILE dev_urandom : T_CHARFILE OPEN read_mode IS "/dev/urandom";

		variable byte : character;
		variable data : STD_LOGIC_VECTOR(0 to 8*n-1) := (others=>'X');
	begin
		for I in 0 to n-1 loop
			read(dev_urandom, byte);
			data(8*I to 8*I+7) := std_logic_vector(to_unsigned(character'pos(byte), 8));
		end loop;
		return data;
	end function;
end package body;
