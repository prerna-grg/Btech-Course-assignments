/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
//package javaapplication1;

import java.io.Serializable;
import java.util.Collection;
import javax.persistence.Basic;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.NamedQueries;
import javax.persistence.NamedQuery;
import javax.persistence.OneToMany;
import javax.persistence.Table;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlTransient;

/**
 *
 * @author prerna
 */
@Entity
@Table(name = "Contact_information")
@XmlRootElement
@NamedQueries({
    @NamedQuery(name = "Contactinformation.findAll", query = "SELECT c FROM Contactinformation c")
    , @NamedQuery(name = "Contactinformation.findById", query = "SELECT c FROM Contactinformation c WHERE c.id = :id")
    , @NamedQuery(name = "Contactinformation.findByStreetAddress", query = "SELECT c FROM Contactinformation c WHERE c.streetAddress = :streetAddress")
    , @NamedQuery(name = "Contactinformation.findByCity", query = "SELECT c FROM Contactinformation c WHERE c.city = :city")
    , @NamedQuery(name = "Contactinformation.findByState", query = "SELECT c FROM Contactinformation c WHERE c.state = :state")
    , @NamedQuery(name = "Contactinformation.findByCountry", query = "SELECT c FROM Contactinformation c WHERE c.country = :country")
    , @NamedQuery(name = "Contactinformation.findByPostalCode", query = "SELECT c FROM Contactinformation c WHERE c.postalCode = :postalCode")
    , @NamedQuery(name = "Contactinformation.findByPhone", query = "SELECT c FROM Contactinformation c WHERE c.phone = :phone")
    , @NamedQuery(name = "Contactinformation.findByMobile", query = "SELECT c FROM Contactinformation c WHERE c.mobile = :mobile")
    , @NamedQuery(name = "Contactinformation.findByEmail", query = "SELECT c FROM Contactinformation c WHERE c.email = :email")})

public class Contactinformation implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "ID")
    private Integer id;
    @Column(name = "StreetAddress")
    private String streetAddress;
    @Column(name = "City")
    private String city;
    @Column(name = "State")
    private String state;
    @Column(name = "Country")
    private String country;
    @Column(name = "PostalCode")
    private String postalCode;
    @Column(name = "Phone")
    private String phone;
    @Column(name = "Mobile")
    private String mobile;
    @Column(name = "Email")
    private String email;
    @OneToMany(mappedBy = "office")
    private Collection<Team> teamCollection;
    @OneToMany(mappedBy = "contact")
    private Collection<Person> personCollection;

    public Contactinformation() {
    }

    public Contactinformation(Integer id) {
        this.id = id;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getStreetAddress() {
        return streetAddress;
    }

    public void setStreetAddress(String streetAddress) {
        this.streetAddress = streetAddress;
    }

    public String getCity() {
        return city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public String getCountry() {
        return country;
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public String getPostalCode() {
        return postalCode;
    }

    public void setPostalCode(String postalCode) {
        this.postalCode = postalCode;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getMobile() {
        return mobile;
    }

    public void setMobile(String mobile) {
        this.mobile = mobile;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    @XmlTransient
    public Collection<Team> getTeamCollection() {
        return teamCollection;
    }

    public void setTeamCollection(Collection<Team> teamCollection) {
        this.teamCollection = teamCollection;
    }

    @XmlTransient
    public Collection<Person> getPersonCollection() {
        return personCollection;
    }

    public void setPersonCollection(Collection<Person> personCollection) {
        this.personCollection = personCollection;
    }

    @Override
    public int hashCode() {
        int hash = 0;
        hash += (id != null ? id.hashCode() : 0);
        return hash;
    }

    @Override
    public boolean equals(Object object) {
        // TODO: Warning - this method won't work in the case the id fields are not set
        if (!(object instanceof Contactinformation)) {
            return false;
        }
        Contactinformation other = (Contactinformation) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "javaapplication1.Contactinformation[ id=" + id + " ]";
    }
    
}
