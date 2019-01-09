isOS(200,Ubuntu,16.04,64,2000,1000,['lxml', 'gcc', 'foo', 'bar']).
isOS(201,Fedore,23,32,1500,700,['lib_a', 'lib_b', 'lib_image', 'bar']).
isMachine(120,'Physical',200,16384.0,6144.0,16).
isMachine(121,'Virtual',201,4096.0,256.0,2).
isApp(300,'MySQL Server',512.0,4.0,2,[200, 201],['lxml', 'gcc', 'foo', 'bar']).
isApp(300,'Apache Web Server',512.0,1.0,2,[200],['lib_a', 'gcc', 'lib_b', 'bar']).
isApp(300,'ImageProcessing Server',2.0,100.0,8,[200],['keras', 'gcc', 'lib_image', 'bar']).

found(X,[X|Tail]).
found(X,[_|Tail]):- found(X,Tail).

subs([], _).
subs([X|Tail], Y):- found(X, Y),subs(Tail, Y).

findMachine(X,L):-isApp(X,A,B,C,D,E,F),isMachine(L,M,N,O,P,Q),O>=B,P>=C,Q>=D,isOS(N,_,_,_,_,_,W),subset(F,W),write("\nID: "),write(L),write("\nType: "),write(M),write("\nOS: "),write(N),write("\nRAM: "),write(O),write(" MB\ndisk: "),write(P),write("GB\nCPU: "),write(Q),write(" cores"),write("\n").

checkAppMachine(X,Y,Y):-isApp(X,_,B,C,D,_,F),isMachine(Y,M,N,O,P,Q),O>=B,P>=C,Q>=D,isOS(N,_,_,_,_,_,W),subset(F,W).
