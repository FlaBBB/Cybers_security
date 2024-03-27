library ieee;
use ieee.std_logic_1164.all;

package rng is
	component pwd_gen is
		generic(
			STATE_SIZE  : POSITIVE := 64;
			OUTPUT_SIZE : POSITIVE := 128
		);
		port(
			CLK    :  in STD_LOGIC;
			RESET  :  in STD_LOGIC;
			ENABLE :  in STD_LOGIC;
			SEED   :  in STD_LOGIC_VECTOR(0 to STATE_SIZE-1);
			TAPPED :  in STD_LOGIC_VECTOR(0 to STATE_SIZE-1);
			VALID  : out STD_LOGIC;
			DATA   : out STD_LOGIC_VECTOR(OUTPUT_SIZE-1 downto 0) := (others => '0')
		);
	end component;
end package;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity pwd_gen is
	generic(
		STATE_SIZE   : POSITIVE := 64;
		OUTPUT_SIZE : POSITIVE := 128
	);
	port(
		CLK    :  in STD_LOGIC;
		RESET  :  in STD_LOGIC;
		ENABLE :  in STD_LOGIC;
		SEED   :  in STD_LOGIC_VECTOR(0 to STATE_SIZE-1);
		TAPPED :  in STD_LOGIC_VECTOR(0 to STATE_SIZE-1);
		VALID  : out STD_LOGIC;
		DATA   : out STD_LOGIC_VECTOR(OUTPUT_SIZE-1 downto 0) := (others => '0')
	);
end pwd_gen;

architecture Behavioral of pwd_gen is
	signal running : BOOLEAN := false;
	signal taps    : STD_LOGIC_VECTOR(0 to STATE_SIZE-1);
	signal state   : STD_LOGIC_VECTOR(0 to STATE_SIZE-1);
	
	signal outbit : STD_LOGIC;
begin
	outbit <= state(STATE_SIZE-1);

	process(CLK) is
		variable counter : INTEGER;
		variable xbit    : STD_LOGIC;
	begin
		if RESET = '1' then
			state <= SEED;
			taps <= TAPPED;
			running <= false;
			counter := 0;
			VALID <= '0';					
		elsif rising_edge(CLK) then
			VALID <= '0';
			if ENABLE = '1' then
				running <= true;
			end if;
			
			if running then				
				state <= (xor (state and taps)) & state(0 to STATE_SIZE-2);
				DATA <= DATA(OUTPUT_SIZE-2 downto 0) & outbit;
				counter := counter + 1;
				
				if counter >= OUTPUT_SIZE then
					VALID <= '1';
					running <= false;
					counter := 0;
				end if;				
			end if;
		end if;
	end process;
end Behavioral;
