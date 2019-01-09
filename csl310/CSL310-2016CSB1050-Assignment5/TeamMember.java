/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
//package javaapplication1;

import java.io.Serializable;
import java.util.Date;
import javax.persistence.Basic;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.NamedQueries;
import javax.persistence.NamedQuery;
import javax.persistence.NamedNativeQuery;
import javax.persistence.NamedNativeQueries;
import javax.persistence.Table;
import javax.persistence.Temporal;
import javax.persistence.TemporalType;
import javax.xml.bind.annotation.XmlRootElement;

/**
 *
 * @author prerna
 */
@Entity
@Table(name = "Team_Member")
@XmlRootElement
@NamedQueries({
    @NamedQuery(name = "TeamMember.findAll", query = "SELECT t FROM TeamMember t")
    , @NamedQuery(name = "TeamMember.findByMemberID", query = "SELECT t FROM TeamMember t WHERE t.memberID = :memberID")
    , @NamedQuery(name = "TeamMember.findBySalary", query = "SELECT t FROM TeamMember t WHERE t.salary = :salary")
    , @NamedQuery(name = "TeamMember.findByHireDate", query = "SELECT t FROM TeamMember t WHERE t.hireDate = :hireDate")
    , @NamedQuery(name = "TeamMember.findByRole", query = "SELECT t FROM TeamMember t WHERE t.role = :role")
    , @NamedQuery(name = "TeamMember.findByRemarks", query = "SELECT t FROM TeamMember t WHERE t.remarks = :remarks")})
    
@NamedNativeQueries({
	@NamedNativeQuery(name = "TeamMember.findAvgStateSalary", query = "SELECT AVG(Salary) FROM Team_Member INNER JOIN (SELECT PersonID FROM Person INNER JOIN (SELECT ID from Contact_information WHERE State=?1)alias1 ON alias1.ID = Person.Contact)alias2 ON alias2.PersonID = Team_Member.PersonID")
    , @NamedNativeQuery(name = "TeamMember.findPlayersInSalaryRange", query = "SELECT First_name,Last_name, HireDate, Salary FROM Person INNER JOIN (SELECT PersonID,Salary,HireDate from Team_Member INNER JOIN  (SELECT TeamID from Team WHERE Name=?1 )alias1 ON alias1.TeamID=Team_Member.TeamID WHERE Salary BETWEEN ?2 AND ?3 AND Role='Player')alias2 ON Person.PersonID = alias2.PersonID")
    , @NamedNativeQuery(name = "TeamMember.findCountByRole" , query = "SELECT Role,COUNT(MemberID) from Team_Member INNER JOIN  (SELECT TeamID from Team WHERE Name=?1 )alias1 ON alias1.TeamID=Team_Member.TeamID GROUP BY Role")})
    
public class TeamMember implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "MemberID")
    private Integer memberID;
    @Column(name = "Salary")
    private Integer salary;
    @Column(name = "HireDate")
    @Temporal(TemporalType.DATE)
    private Date hireDate;
    @Column(name = "Role")
    private String role;
    @Column(name = "Remarks")
    private String remarks;
    @JoinColumn(name = "PersonID", referencedColumnName = "PersonID")
    @ManyToOne
    private Person personID;
    @JoinColumn(name = "TeamID", referencedColumnName = "TeamID")
    @ManyToOne
    private Team teamID;

    public TeamMember() {
    }

    public TeamMember(Integer memberID) {
        this.memberID = memberID;
    }

    public Integer getMemberID() {
        return memberID;
    }

    public void setMemberID(Integer memberID) {
        this.memberID = memberID;
    }

    public Integer getSalary() {
        return salary;
    }

    public void setSalary(Integer salary) {
        this.salary = salary;
    }

    public Date getHireDate() {
        return hireDate;
    }

    public void setHireDate(Date hireDate) {
        this.hireDate = hireDate;
    }

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }

    public String getRemarks() {
        return remarks;
    }

    public void setRemarks(String remarks) {
        this.remarks = remarks;
    }

    public Person getPersonID() {
        return personID;
    }

    public void setPersonID(Person personID) {
        this.personID = personID;
    }

    public Team getTeamID() {
        return teamID;
    }

    public void setTeamID(Team teamID) {
        this.teamID = teamID;
    }

    @Override
    public int hashCode() {
        int hash = 0;
        hash += (memberID != null ? memberID.hashCode() : 0);
        return hash;
    }

    @Override
    public boolean equals(Object object) {
        // TODO: Warning - this method won't work in the case the id fields are not set
        if (!(object instanceof TeamMember)) {
            return false;
        }
        TeamMember other = (TeamMember) object;
        if ((this.memberID == null && other.memberID != null) || (this.memberID != null && !this.memberID.equals(other.memberID))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "javaapplication1.TeamMember[ memberID=" + memberID + " ]";
    }
    
}
